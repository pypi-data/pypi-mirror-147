import re
import os
import logging
import io
import boto3

import awswrangler as wr
import pydbtools as pydb

from collections import Counter
from copy import deepcopy
from typing import Tuple, Union, List, Any
from mojap_metadata.converters.arrow_converter import ArrowConverter
from mojap_metadata.converters.glue_converter import (
    GlueConverter,
    _default_type_converter,
)
from pyarrow import Schema
from mojap_metadata.metadata.metadata import (
    Metadata, 
    _get_type_category_pattern_dict_from_schema
)
from arrow_pd_parser import reader
from dataengineeringutils3.s3 import(
    get_filepaths_from_s3_folder,
    delete_s3_folder_contents,
)


def _logging_setup() -> logging.Logger:

    global loggers

    if loggers.get("root"):
        return loggers.get("root")
    else:
        log = logging.getLogger("root")
        log.setLevel(logging.DEBUG)

        log_stringio = io.StringIO()
        handler = logging.StreamHandler(log_stringio)

        log_formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(log_formatter)
        log.addHandler(handler)

        # Add console output
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(log_formatter)
        log.addHandler(console)
        loggers["root"] = log

        return log


def _warn_on_change(
    warn_msg: str,
    new: Union[str, None],
    old: Union[str, None],
    has_been_made: bool=False
):
    if old is not None and new != old:
        _logger.info(warn_msg)
    if has_been_made:
        _logger.info(
            "The table(s) have already been created, this change may not take effect or"
            " have untwanted consequences"
        )


def _validate_string(
    s: str, error_name: str, char_set: str="", len_reqs: str="", alt_regex: str=None
):

    # is it a string?
    if not isinstance(s, str):
        raise ValueError(f"{error_name} must be a string, found {type(s)}")

    # is this string a reserved name?
    if s in dir(Athena) or s in dir(AthenaTable) or s in dir(AthenaDatabase):
        raise ValueError(f"value {s} for {error_name} is a reserved name")

    # default allows lowercase characters a-z and underscores only
    regex_pattern = f"^[a-z0-9_{char_set}]{len_reqs}$" if not alt_regex else alt_regex
    if not re.match(regex_pattern, s):
        raise ValueError(
            f"malformed {error_name} - must fit regex: {regex_pattern}. failed: {s}"
        )


def _are_required_attrs_set(attr_dict: dict):
    non_set_attrs = None
    required_attrs_are_set = False
    ks = list(attr_dict.keys())
    vs = list(attr_dict.values())
    non_set_attrs = [v for i, v in enumerate(ks) if vs[i] is None]
    if non_set_attrs:
        _logger.info(f"required attributes not set: {', '.join(non_set_attrs)}")
    else:
        required_attrs_are_set = True

    return required_attrs_are_set


def _delete_glue_table(db_name: str, table_name: str):
    wr.catalog.delete_table_if_exists(database=db_name, table=table_name)


def _generate_boto_dict(
    metadata: Metadata, db_name: str, table_location: str, skip_header: bool
):
    gc = GlueConverter()
    if metadata.file_format == "csv":
        gc.options.csv.skip_header = skip_header
    return gc.generate_from_meta(
        metadata, database_name=db_name, table_location=table_location
    )


def _get_file_format(pth: str): # pth has "s3://"" infront
    # are there any files for us to infer from?
    files_in_path = get_filepaths_from_s3_folder(pth)
    if not len(files_in_path):
        raise ValueError(
            f"no file format specified in metadata, and no files to infer from in {pth}"
        )
    
    # there are files to infer from, but do they all have the same ff?
    ff_list = [os.path.splitext(f)[1][1:] for f in files_in_path]
    found_ffs = list(Counter(ff_list).keys())
    if len(found_ffs) != 1:
        raise ValueError(
            "no file format specified in metadata, and found more than one file format "
            f"in {pth}: {', '.join(found_ffs)}"
        )
    
    return found_ffs[0]
    

def _path_setter(
    new_path: str, old_path: Union[str, None], 
    has_been_made: bool, obj_name: str
):
    if new_path is None and old_path is not None:
        _logger.info("removing db_base_path")
    else:
        _validate_string(
            new_path, "db base path", char_set="A-Z0-9.\-/:", len_reqs="+"
        )
    
    # remove any leading and trailing slashes that might exist
    while new_path.startswith("/"):
        new_path = new_path[1:]
    while new_path.endswith("/"):
        new_path = new_path[:-1]
    # remove s3 prefix, if it exists (and then put it back in later lmao)
    if new_path.startswith("s3://"):
        new_path = new_path.replace("s3://", "")

    warn_msg = f"changing {obj_name} from {old_path} to {new_path}"
    _warn_on_change(
        warn_msg, new_path, old_path, has_been_made=has_been_made
    )

    return new_path


def _db_name_setter(
    new_db_name: str, old_db_name: Union[str, None], has_been_made: bool
):
    if new_db_name is None and old_db_name is not None:
        _logger.info("removing db_name")
    else:
        _validate_string(new_db_name, "database name", len_reqs="+")

    warn_msg = f"changing db_name from \"{old_db_name}\" to \"{new_db_name}\""
    _warn_on_change(warn_msg, new_db_name, old_db_name, has_been_made=has_been_made)

    return new_db_name


def _partitions_setter(
    new_partions: List[dict], old_paritions: Union[List[dict], None], has_been_made: bool
):
    if new_partions is None:
        if old_paritions is not None:
            _logger.info("removing partitions")
        return new_partions

    # example: [{"name": "part_name", "type": "part_type", "value": "part_val"}]
    if not isinstance(new_partions, list) or not \
        all(isinstance(p, dict) for p in new_partions):
        raise ValueError("partitions not correctly format, must be a list of dicts")

    required_keys = ["name", "type", "value"]

    for partition in new_partions:

        key_list = list(partition.keys())

        # does the partition contain the required keys?
        if Counter(key_list) != Counter(required_keys):
            keys_missing = [k for k in required_keys if k not in key_list]
            raise ValueError(
                f"partition dict missing keys: {', '.join(keys_missing)} for partition "
                f"{partition}"
            )

        # does the partition contain keys that AREN'T in the required keys?
        unsupported_keys = [k for k in key_list if k not in required_keys]
        if unsupported_keys:
            raise ValueError(
                f"unsupport keys in partitions: {', '.join(unsupported_keys)} for "
                f"partition {partition}"
            )

        # do the values conform?
        _validate_string(
            partition["name"], 
            f"partition name: {partition['name']}", 
            char_set="A-Z\-", 
            len_reqs="+"
        )
        type_re = "|".join(list(_get_type_category_pattern_dict_from_schema().values()))
        _validate_string(
            partition["type"], 
            f"partition type: {partition['type']}", 
            alt_regex=type_re
            )
        _validate_string(
            partition["value"], 
            f"partition value: {partition['type']}", 
            char_set="A-Z\-", len_reqs="+"
        )

    # ok probably sure it's ok now
    warn_msg = f"changing partitions from {old_paritions} to {new_partions}"
    _warn_on_change(warn_msg, new_partions, old_paritions, has_been_made=has_been_made)

    return new_partions


def _database_folder_name_setter(
    new_folder_name: str, old_folder_name: str, has_been_made: bool
):
    _validate_string(
        new_folder_name, "database folder name", 
        char_set="A-Z\-", 
        len_reqs="+"
    )
    warn_msg = (
        f"changing database folder name from {old_folder_name} "
        f"to {new_folder_name}"
    )
    _warn_on_change(
        warn_msg, 
        new_folder_name, 
        old_folder_name, 
        has_been_made
    )

    return new_folder_name


loggers = {}
_logger = _logging_setup()

class Athena:

    def __init__(self):
        self._databases = []
        self.csv_skip_header = True

    def add_db(self, db):

        if isinstance(db, str):
            db_name = db
            db = self._make_athena_db_from_str(db_name)
        elif isinstance(db, AthenaDatabase):
            if not db.db_name:
                raise ValueError("cannot add database without a name!")
            elif db.db_name in self._databases:
                raise ValueError(f"database already defined {db.db_name}")
            else:
                db_name = db.db_name
                self._databases.append(db_name)

        setattr(self, db_name, db)

    def _make_athena_db_from_str(self, db_name):
        _validate_string(db_name, "database name", len_reqs="+")
        if db_name in self._databases:
            raise ValueError(f"database already defined: {db_name}")
        elif db_name in dir(AthenaDatabase):
            raise ValueError(f"db name {db_name} is a reserved name")
        elif not _are_required_attrs_set(
            attrs := {
                "csv_skip_header": self.csv_skip_header
            }
        ):
            _logger.info("please set required attributes")
        else:
            attrs["db_name"] = db_name
            self._databases.append(db_name)
            new_database = AthenaDatabase(**attrs)
            return new_database

    def create_all_tables(self):
        for db_name in self._databases:
            db = getattr(self, db_name)
            db.create_all_tables()

    def nuke_all(self):
        # deletes everything, data and glue tables
        for db_name in self._databases:
            db = getattr(self, db_name)
            db.nuke_all()

    def delete_all_tables(self):
        # deletes glue tables only
        for db_name in self._databases:
            db = getattr(self, db_name)
            db.delete_all_tables()

    def overlay_all_schemas(self):
        for db_name in self._databases:
            db = getattr(self, db_name)
            db.overlay_all_schemas()

    @property
    def csv_skip_header(self):
        return self._csv_skip_header
    
    @csv_skip_header.setter
    def csv_skip_header(self, skip_header: bool):
        if not isinstance(skip_header, bool):
            raise TypeError(
                f"csv skip header must be of type bool, found: {type(skip_header)}"
            )
        self._csv_skip_header = skip_header

class AthenaDatabase:

    def __init__(self, **kwargs):
        self._db_name = None
        self._db_base_path = None
        self._partitions = None
        self.csv_skip_header = True
        self._database_folder_name = "database"

        self._table_names = []

        self._database_has_been_made = False

        if (db_name := kwargs.get("db_name")):
            self.db_name = db_name
        if (db_base_path := kwargs.get("db_base_path")):
            self.db_base_path = db_base_path
        if (partitions := kwargs.get("partitions")):
            self.partitions = partitions
        if (csv_skip_header := kwargs.get("csv_skip_header")) is not None:
            self.csv_skip_header = csv_skip_header
    
    def add_table(self, inp):
        if isinstance(inp, str):
            table_name = inp
            table = self._make_athena_table_from_str(table_name)
        elif isinstance(inp, AthenaTable):
            table = inp
            if not table.table_name:
                raise ValueError("cannot add table with no name")
            elif table.table_name in self._table_names:
                raise ValueError(f"table already defined: {table.table_name}")
            else:
                table_db_name = table.db_name
                if table_db_name != self.db_name:
                    # this should _really_ error
                    _logger.info(
                        f"AthenaTable {table.table_name} has a different table name"
                    )
                table_name = table.table_name
                self._table_names.append(table_name)
        else:
            raise TypeError(f"unknown type for table: {type(inp)}")

        setattr(self, table_name, table)

    def create_all_tables(self):
        for table_name in self._table_names:
            table = getattr(self, table_name)
            table.create_table()
        self.database_has_been_made = True

    def delete_all_tables(self):
        # deletes glue tables only
        if not _are_required_attrs_set({"db name": self.db_name}):
            _logger.info("please set required attributes")
        else:
            for table_name in self._table_names:
                table = getattr(self, table_name)
                table.delete_table()

    def nuke_all(self):
        # deletes everything, data and glue tables
        if not _are_required_attrs_set({"db name": self.db_name}):
            _logger.info("please set required attributes")
        else:
            for table_name in self._table_names:
                table = getattr(self, table_name)
                table.nuke()
            try:
                wr.catalog.delete_database(name=self.db_name)
                _logger.info(f"The database: {self.db_name} deleted")
            except Exception as e:
                _logger.info(f"database did not exist: {self.db_name}")

    def overlay_all_schemas(self):
        if not _are_required_attrs_set({"db name": self.db_name}):
            _logger.info("please set required attributes")
        else:
            for table_name in self._table_names:
                table = getattr(self, table_name)
                table.overlay_schema()

    def set_table_attributes(self, table_list = None):
        table_list = self._table_names if not table_list else table_list
        # are all the table names really there?
        non_existing_tables = [t for t in table_list if t not in self._table_names]
        if non_existing_tables:
            raise ValueError(
                "tables specified are not part of this db: "
                f"{', '.join(non_existing_tables)}"
            )
        
        # all the tables are there, set attrs one by one, inducing any log changes etc
        # this will null out some values 
        for table_name in table_list:
            table = getattr(self, table_name)
            table.db_name = self.db_name
            table.db_base_path = self.db_base_path
            table.partitions = self.partitions
            table.database_folder_name = self.database_folder_name
            table.csv_skip_header = self.csv_skip_header

    def _make_athena_table_from_str(self, table_name):
        if table_name in self._table_names:
            raise ValueError(f"table {table_name} already exists")
        elif not _are_required_attrs_set(
            attrs := {
                "db_name": self.db_name, 
                "db_base_path": self.db_base_path, 
                "database_folder_name": self.database_folder_name,
                "csv_skip_header": self.csv_skip_header,
            }
        ):
            _logger.info("please set required attributes")
        else:
            self._table_names.append(table_name)
            # do we want to inherit partitions?
            if self.partitions is not None:
                attrs["partitions"] = self.partitions
            new_table = AthenaTable(**attrs)
            new_table.table_name = table_name
            return new_table

    @property
    def db_name(self):
        return self._db_name

    @db_name.setter
    def db_name(self, db_name: str):
        self._db_name = _db_name_setter(
            db_name, self._db_name, self._database_has_been_made
        )

    @property
    def db_base_path(self):
        return self._db_base_path

    @db_base_path.setter
    def db_base_path(self, db_base_path):
        self._db_base_path = _path_setter(
            db_base_path, self._db_base_path, self._database_has_been_made, "db_base_path"
        )
    
    @property
    def partitions(self):
        return self._partitions
    
    @partitions.setter
    def partitions(self, partitions):
        self._partitions = _partitions_setter(
            partitions, self._partitions, self._database_has_been_made
        )

    @property
    def database_folder_name(self):
        return self._database_folder_name

    @database_folder_name.setter
    def database_folder_name(self, database_folder_name: str):
        self._database_folder_name = _database_folder_name_setter(
            database_folder_name,
            self._database_folder_name,
            self._database_has_been_made
        )
   
    @property
    def csv_skip_header(self):
        return self._csv_skip_header
    
    @csv_skip_header.setter
    def csv_skip_header(self, skip_header: bool):
        if not isinstance(skip_header, bool):
            raise TypeError(
                f"csv skip header must be of type bool, found: {type(skip_header)}"
            )
        self._csv_skip_header = skip_header

class AthenaTable:

    def __init__(self, **kwargs):
        # partitions, _db_name, and _db_base_path can be "inherited"
        self._db_name = None
        self._db_base_path = None
        self._partitions = None
        self._table_name = None
        self._data_path = None
        self._table_metadata = None
        self._arrow_schema = None
        self._original_partition_names = None

        self._write_mode = "append"
        self._database_folder_name = "database"

        self._partition_data = False
        self._csv_skip_header = True
        self._user_has_specified_meta = False
        self._df = None
        self._df_sample = None

        self._ready_to_create_database = False
        self._table_has_been_made = False
        self._warn_on_data_already_exists = True
        self._warn_on_nuke = True

        if (db_name := kwargs.get("db_name")):
            self.db_name = db_name
        if (db_base_path := kwargs.get("db_base_path")):
            self.db_base_path = db_base_path
        if (partitions := kwargs.get("partitions")):
            self.partitions = partitions
        if (table_name := kwargs.get("table_name")):
            self.table_name = table_name
        if (data_path := kwargs.get("data_path")):
            self.data_path = data_path
        if (write_mode := kwargs.get("write_mode")):
            self.write_mode = write_mode
        if (database_folder_name := kwargs.get("database_folder_name")):
            self.database_folder_name = database_folder_name
        if (table_metadata := kwargs.get("table_metadata")):
            self.table_metadata = table_metadata
        if (csv_skip_header := kwargs.get("csv_skip_header")) is not None:
            self.csv_skip_header = csv_skip_header

    def create_table(self):
        # check all the data is set and ready for creation
        if not _are_required_attrs_set(
            {
                "db_name": self.db_name,
                "table_name": self.table_name,
                "db_base_path": self._db_base_path,
                "data_path": self.data_path
            }
        ):
            raise ValueError("please set required attributes")

        # does it already end in /database?
        if self.db_base_path.endswith(("database", "database/")):
            _logger.info("db base path already ends in \"database\"")
            self.database_folder_name = ""

        self._s3_db_path = (
            f"s3://{os.path.join(self.db_base_path, self._database_folder_name)}"
        )
        self._s3_table_path = (
            f"{self._s3_db_path}/{self.table_name}"
        )

        data_is_present_in_table_location = any(
            get_filepaths_from_s3_folder(self._s3_table_path)
        )

        if (
            self._warn_on_data_already_exists
            and data_is_present_in_table_location
            and self.write_mode != "append"
        ):
            _logger.info(
                "Data is present in table location - this may delete data"
                )
            self._warn_on_data_already_exists = False

        # make the database if it doesn't already exist
        self._make_database_if_not_exists()

        self._copy_data_to_database_location()
        self._table_has_been_made = True
        _logger.info(f"table succesfully created: {self.table_name}")

    def overlay_schema(self):
        # check all required attributes are set
        if not _are_required_attrs_set(
            {

                "csv skip header": self.csv_skip_header,
            }
        ):
            raise ValueError("please set required attributes")

        # use db_base_path for schema overlaying
        pth = f"s3://{self.db_base_path}/{self.table_name}"

        # get file format, if not specified
        if not self.table_metadata.file_format:
            ff = _get_file_format(pth)
            _logger.info(f"no file format specified in meta, set to: {ff}")
            self.table_metadata.file_format = ff

        # delete glue table, if it exists
        _delete_glue_table(self.db_name, self.table_name)

        # make the database if it doesn't already exist
        self._make_database_if_not_exists()

        _logger.info(f"overlaying schema on path: {pth}")

        # generate the glue schema
        boto_dict = _generate_boto_dict(
            self.table_metadata, self.db_name, pth, self.csv_skip_header
        )

        # overlay schema
        glue_client = boto3.client("glue")
        glue_client.create_table(**boto_dict)

        # repair, incase
        pydb.read_sql_query(f"msck repair table {self.db_name}.{self.table_name}")

        self._table_has_been_made = True

    # FIX FFIX FIXFIWEFWE
    def nuke(self):
        # FIX: broken s3 path, because of the database_folder_name (may already be set)
        # deletes everything, data and glue tables
        if not _are_required_attrs_set(
            {
                "db name": self.db_name,
                "table name": self.table_name,
                "db base path": self.db_base_path
            }
        ):
            _logger.info("Please set required attributes")
        else:
            s3_path = (
                f"s3://{self.db_base_path}/{self.database_folder_name}/"
                f"{self.table_name}"
            )
            # delete glue table
            _logger.info(f"deleting glue table: {self.db_name}.{self.table_name}")
            _delete_glue_table(self.db_name, self.table_name)
            # delete s3 data
            _logger.info(f"deleting data: {s3_path}")
            delete_s3_folder_contents(s3_path)

    def delete_table(self):
        # deletes glue table only
        if not _are_required_attrs_set(
            {
                "db name": self.db_name,
                "table name": self.table_name,
            }
        ):
            _logger.info("please set required attributes")
        else:
            _delete_glue_table(self.db_name, self.table_name)
            _logger.info(f"deleted table: {self.db_name}.{self.table_name}")

    def _get_existing_partitions_if_exists(self):

        existing_partitions = None

        # does the table even exist?
        if not wr.catalog.does_table_exist(
            database=self.db_name, table=self.table_name
        ):
            return
        # do we even have partition data?
        if not self.partition_data:
            return
        
        # ok so we have partition data, and the table exists. 
        # we now need to order the columns and partitions in the correct order

        # what are all the juicy details of the table?
        table_iterator =  wr.catalog.get_tables(
            database=self.db_name, name_contains=self.table_name
        )
        found_table_details = False
        for table in table_iterator:
            # is this our table? kinda annoying that I cant specify the exact table
            # none of: table, get_table_parameters, get_table_description, give enough
            if table["Name"] != self.table_name:
                continue
            # have I already found the details? i.e. are there duplicate tables? 
            # unlikley I think, but not a hard check
            if found_table_details:
                raise ValueError(
                    f"mulitple tables with name {self.table_name} "
                    f"found in db {self.table_name}"
                )
            # capture the existing partitions, these are in order
            existing_partitions = table["PartitionKeys"]
            existing_partitions_names_only = [d["Name"] for d in existing_partitions]
            found_table_details = True
        
        # no point running if there's no data to run on
        if not existing_partitions and not self.partition_data:
            return

        # this is the case where the table already exists, has no partitions and you
        # want to add them (not really viable)
        if not existing_partitions and self.partition_data:
            raise ValueError("Cannot add partitions to existing table")

        partitions_names_only = [d["name"] for d in self.partitions]
        # if the existing partitions don't exactly match the ones specced, error
        if Counter(partitions_names_only) != Counter(existing_partitions_names_only):
            raise ValueError(
                f"existing table {self.table_name} has non matching partitions: "
                f"specified: \"{', '.join(partitions_names_only)}\" "
                f"existing table: \"{', '.join(existing_partitions_names_only)}\""
            )

        if partitions_names_only != existing_partitions_names_only:
            _logger.info(
                "partitions specified not in the correct order, attempting to rectify"
            )

        # all the partitions match so we now have 2 more questions:
        #   1. is self.partitions in the correct order? if not, make it so
        #   2. are the columns in the metadata in the right order? if not, make it so!
        new_partitions = []
        for partition in existing_partitions:
            # get the matching specced partition
            matching_partitions = [
                {k:v for k,v in d.items()} for d in self.partitions
                if d["name"] == partition["Name"]
            ]
            # for some reason, if there isn't one and only one, error
            if len(matching_partitions) != 1:
                raise ValueError("somehow, there are more than one matching partitions")
            matching_partition = matching_partitions[0]

            # the types should also match, otherwise wtf are you doing
            new_type = matching_partition["type"]
            old_type = partition["Type"]
            if not _default_type_converter[new_type][0] == old_type:
                raise TypeError(
                    f"partition type for partion {partition['Name']} for {self.db_name}"
                    f".{self.table_name} is incompatible with existing partition type"
                )

            # now we know this partition is all ok, add it to the new_partitions
            new_partitions.append(matching_partition)

        # so we have partitions in the right order (new_partitions)
        # it's time to order the metadata (there is always metadata at this point)
        meta_col_partition_indexes = []
        meta_cols = self.table_metadata.columns
        for i, col in enumerate(meta_cols):
            if col["name"] in partitions_names_only:
                meta_col_partition_indexes.append(i)

        # this shouldn't be a possible error, but:
        if len(meta_col_partition_indexes) != len(new_partitions):
            raise ValueError("metadata missing partitions in columns")

        # we now know where all of our partitions are in the metadata columns
        # remove and re-order them
        removed_meta_cols = []
        meta_col_partition_indexes.reverse()
        for i in meta_col_partition_indexes:
            removed_meta_cols.append(self.table_metadata.columns.pop(i))

        # now add them in the order they are in (the correctly ordered) new_partitions
        for partition in new_partitions:
            name = partition["name"]
            matching_meta_cols = [{k:v for k,v in d.items()} for d in removed_meta_cols if d["name"] == name]
            if len(matching_meta_cols) != 1:
                raise ValueError("somehow, there isn't exaclty one matching meta col")
            matching_meta_col = matching_meta_cols[0]
            self.table_metadata.columns.append(matching_meta_col)

        # make the partitions part in the right order, but I don't think this matters
        new_partitions_names_only = [d["name"] for d in new_partitions]
        self.table_metadata.partitions = new_partitions_names_only

        # finally, set self._partitions
        self._partitions = new_partitions

    def _set_partitions_if_required(self):
        # set partitions if required
        if self.partition_data:

            # get the new partition names
            parition_names_only = [c["name"] for c in self.partitions]

            # get the partitions names and types as a dict (will need this later) tag
            partitions_name_and_type = [
                {k:v for k,v in d.items() if k != "value"} for d in self.partitions
            ]

            # collect the information about the current partitions defined
            old_partitions_names_only = self.table_metadata.partitions
            old_partitions = [
                {k:v for k,v in d.items()} for d in self.table_metadata.columns if
                d["name"] in old_partitions_names_only
            ]
            old_column_names_only = [d["name"] for d in self.table_metadata.columns]
            old_columns_sans_partitions = [
                k for k in old_column_names_only 
                if k not in old_partitions_names_only
            ]

            # are any of the new partitions columns already (but not partitions)?
            common_col_partitions = [
                p for p in parition_names_only if p in old_columns_sans_partitions
            ]
            if common_col_partitions:
                raise ValueError(
                    "values specified in partition data exists in columns: " 
                    f"{', '.join(common_col_partitions)}"
                    )
 
            # check any new partition types against old types and error if different
            for partition in partitions_name_and_type:
                matching_old_partition = [
                    {k:v for k,v in d.items()} for d in old_partitions if
                    d["name"] == partition["name"]
                ]

                # just in case
                if len(matching_old_partition) > 1:
                    raise ValueError(
                        "this should not be a reachable error, really. But: "
                        "More than one matching partition found in type checking"
                    )

                if not matching_old_partition:
                    continue
                
                # if it's user specced, allow the change, else error
                old_partition = matching_old_partition[0]
                if old_partition["type"] != partition["type"]:
                    if old_partition["name"] in self._original_partition_names:
                        raise ValueError(
                            f"partition {old_partition['name']} from metadata cannot "
                            "have type changed"
                        )
                    else:
                        _logger.info(f"changing partition type: {partition['name']}")

            # the partition/column make-up seems fine
            # now we need to add only the correct ones to the metadata
            partitions_to_add_names_only = [
                name for name in parition_names_only if
                name not in old_partitions_names_only
            ]
            partitions_to_add_name_and_type = [
                {k:v for k,v in d.items()} for d in partitions_name_and_type if
                d["name"] not in old_partitions_names_only
            ]

            # add the name and types to the columns
            self.table_metadata.columns.extend(partitions_to_add_name_and_type)
            # add partitions names only to partitions
            self.table_metadata.partitions.extend(partitions_to_add_names_only)

    def _make_database_if_not_exists(self):
        try:
            wr.catalog.create_database(self.db_name)
        except Exception:
            pass

    def _make_metadata_and_add_partitions(self):
        _logger.info(
            "partitions have been set, but no metadata - attempting to create metadata"
            )
        # get the arrow schema
        arrow_schema = Schema.from_pandas(self._df)
        # turn it into mojap-metadata object and set the metadata
        ac = ArrowConverter()
        self.table_metadata = ac.generate_to_meta(arrow_schema)
        # table_metadata sets this to true, but this wasn't user specified! 
        self._user_has_specified_meta = False
        # set the partitions if required
        self._set_partitions_if_required()
        _logger.info("metadata and partitions sucessfully merged")

    def _get_out_path(self):
        # is there metadata?
        if self._user_has_specified_meta:
            # has the metadata got partitions and has the user set them?
            if self.table_metadata.partitions and not self.partition_data:
                raise ValueError(
                    "metadata contains partition data but partitions have not been set"
                )
            # ok so are all the partitions set?
            elif self.partition_data:
                user_partitions = [c["name"] for c in self.partitions]
                for partition in self.table_metadata.partitions:
                    if partition not in user_partitions:
                        raise ValueError(
                            f"partition in meta: {partition} has no value defined"
                        )

        fp, fn = os.path.split(self.data_path)
        fn, ff = os.path.splitext(fn)
        out_path =  f"{self._s3_db_path}/{self.table_name}"
        if self.partition_data:
            for partition in self.partitions:
                out_path = os.path.join(out_path, f"{partition['name']}={partition['value']}")
        out_path = os.path.join(out_path, f"{fn}.snappy.parquet")
        return out_path

    def _copy_data_to_database_location(self):

        # the user wants partitions, but has specified no metadata
        if self.partition_data and not self._user_has_specified_meta:
            self._make_metadata_and_add_partitions()

        # refresh metadata - this is incase there is a changing partitions
        if self._user_has_specified_meta:
            _logger.info("trying to refresh metadata before creation")
            self.table_metadata = self.table_metadata
            self._set_partitions_if_required()

        self._get_existing_partitions_if_exists()

        # delete glue table, for laughs
        _delete_glue_table(self.db_name, self.table_name)

        wr.s3.to_parquet(
            df=self._df,
            path=self._get_out_path(),
            index=False,
            dataset=True,
            database=self.db_name,
            table=self.table_name,
            mode=self.write_mode,
        )

        if self.table_metadata is not None:
            _delete_glue_table(self.db_name, self.table_name)
            self.table_metadata.file_format = "parquet"
            boto_dict = _generate_boto_dict(
                self.table_metadata, self.db_name, self._s3_table_path, False
            )
            glue_client = boto3.client("glue")
            glue_client.create_table(**boto_dict)

        if self.partition_data:
            pydb.start_query_execution_and_wait(
                f"msck repair table {self.db_name}.{self.table_name}"
            )

    def _read_data_into_memory(self):
        m = self._table_metadata if self._table_metadata else None
        self._df = reader.read(self.data_path, metadata=m)
        self._df_sample = self._df.head(5)

    @property
    def db_name(self):
        return self._db_name

    # ADD: if db_name and table_name are set, collect existing information and populate it! 
    # I also think ditch the /database thing.
    @db_name.setter
    def db_name(self, db_name: str):
        self._db_name = _db_name_setter(
            db_name, self._db_name, self._table_has_been_made
        )
        if self._user_has_specified_meta:
            _logger.info(f"setting db name in metadata to {db_name}")
            self.table_metadata.name = self.db_name

    @property
    def db_base_path(self):
        return self._db_base_path

    @db_base_path.setter
    def db_base_path(self, db_base_path: str):
        self._db_base_path = _path_setter(
            db_base_path, self._db_base_path, self._table_has_been_made, "db_base_path"
        )

    @property
    def table_name(self):
        return self._table_name

    @table_name.setter
    def table_name(self, new_table_name: str):
        _validate_string(new_table_name, "table name", len_reqs="+")
        warn_msg = (
            f"changing table_name from \"{self.table_name}\" to \"{new_table_name}\""
        )
        _warn_on_change(
            warn_msg, 
            new_table_name, 
            self.table_name, 
            has_been_made = self._table_has_been_made
        )
        self._table_name = new_table_name

    @property
    def data_path(self):
        return self._data_path

    @data_path.setter
    def data_path(self, data_path: str):
        _validate_string(
            data_path, "table data path", 
            char_set="A-Z0-9:\/!\- _.*'()", 
            len_reqs= "+",
        )

        warn_msg = (
            f"changing data_path from {self.data_path} "
            f"to {data_path}"
        )
        _warn_on_change(
            warn_msg, data_path, self.data_path, has_been_made=self._table_has_been_made
        )
        self._data_path = data_path
        self._read_data_into_memory()

    @property
    def write_mode(self):
        return self._write_mode

    @write_mode.setter
    def write_mode(self, user_wm: str):
        wms = ["overwrite", "append", "overwrite_partitions"]
        if user_wm not in wms:
            raise ValueError(f"mode {user_wm} not allowed. Must be: {' or '.join(wms)}")
        warn_msg = f"changing write mode from {self.write_mode} to {user_wm}"
        _warn_on_change(
            warn_msg, user_wm, self.write_mode, has_been_made=self._table_has_been_made
        )
        self._write_mode = user_wm

    @property
    def database_folder_name(self):
        return self._database_folder_name

    @database_folder_name.setter
    def database_folder_name(self, database_folder_name: str):
        self._database_folder_name = _database_folder_name_setter(
            database_folder_name,
            self._database_folder_name,
            self._table_has_been_made
        )

    @property
    def partitions(self):
        return self._partitions
    
    @partitions.setter
    def partitions(self, partitions: List[dict]):
        self._partitions = _partitions_setter(
            partitions, self._partitions, self._table_has_been_made
        )
        if self._partitions:
            self.partition_data = True

    @property
    def partition_data(self):
        return self._partition_data

    @partition_data.setter
    def partition_data(self, partition_data: bool):
        if not isinstance(partition_data, bool):
            raise ValueError("partition_data must be boolean value")
        warn_msg = "changing partition data"
        _warn_on_change(
            warn_msg, 
            str(partition_data), 
            str(self._partition_data), 
            self._table_has_been_made
        )
        self._partition_data = partition_data

    @property
    def table_metadata(self):
        return self._table_metadata

    @table_metadata.setter
    def table_metadata(self, new_metadata: Union[str, dict, Metadata]):
        if isinstance(new_metadata, str):
            if not os.path.isfile(new_metadata):
                raise ValueError("path for metadata not resolvable or doesn't exist")
            elif new_metadata.lower().endswith("json"):
                self._table_metadata = Metadata.from_json(new_metadata)
            elif new_metadata.lower().endswith(("yml", "yaml")):
                self._table_metadata = Metadata.from_yaml(new_metadata)
        elif isinstance(new_metadata, dict):
            self._table_metadata = Metadata.from_dict(new_metadata)
        elif isinstance(new_metadata, Metadata):
            self._table_metadata = new_metadata
        else:
            raise TypeError(
                "Metadata must be str, dict, or Metadata object, "
                f"found : {type(new_metadata)}"
            )
        
        _logger.info("changing metadata")

        # this is so we can tell what is a user added and what is an original metadata
        if not self._user_has_specified_meta:
            self._original_partition_names = deepcopy(self.table_metadata.partitions)
        
        ac = ArrowConverter()
        self._arrow_schema = ac.generate_from_meta(self._table_metadata)

        # if the metadata has the table name in, set it from there
        if table_name := self.table_metadata.name:
            if self.table_name != table_name:
                _logger.info(
                    f"metadata specifies table name as: {table_name}, "
                    f"however it is set as: {self.table_name}"
                )
        elif self.table_name:
            self.table_metadata.name = self.table_name

        self._user_has_specified_meta = True

        # if the data has already been read and then metadata is specified, re-read
        if self._df is not None:
            _logger.info("re-reading data and casting to schema")
            self._read_data_into_memory()

        if self._table_has_been_made:
            _logger.info(
                "The table has already been made - this change may not take affect or "
                "have unintended outcomes."
            )

    @property
    def csv_skip_header(self):
        return self._csv_skip_header
    
    @csv_skip_header.setter
    def csv_skip_header(self, skip_header: bool):
        if not isinstance(skip_header, bool):
            raise TypeError(
                f"csv skip header must be of type bool, found: {type(skip_header)}"
            )
        warn_msg = (
            f"changing csv skip header from {self.csv_skip_header} to {skip_header}"
        )
        _warn_on_change(warn_msg, skip_header, self.csv_skip_header)
        self._csv_skip_header = skip_header

    @property
    def df_sample(self):
        return self._df_sample
