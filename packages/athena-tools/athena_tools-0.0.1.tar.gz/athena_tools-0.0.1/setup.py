# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['athena_tools']

package_data = \
{'': ['*']}

install_requires = \
['arrow-pd-parser>=1.0.4,<2.0.0',
 'dataengineeringutils3>=1.4.0,<2.0.0',
 'mojap-metadata[glue,arrow]>=1.9.4,<2.0.0',
 'pydbtools>=5.2.0,<6.0.0']

setup_kwargs = {
    'name': 'athena-tools',
    'version': '0.0.1',
    'description': 'set of useful Athena db creation tools',
    'long_description': None,
    'author': 'stephen bias',
    'author_email': 'stephen.bias@digital.justice.gov.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
