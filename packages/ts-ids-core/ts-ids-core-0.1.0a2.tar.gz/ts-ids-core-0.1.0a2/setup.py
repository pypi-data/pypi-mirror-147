# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ts_ids_core', 'ts_ids_core.base', 'ts_ids_core.scripts']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0', 'pydantic>=1.8,<2', 'typing-extensions>=4.0']

entry_points = \
{'console_scripts': ['export-schema = '
                     'ts_ids_core.scripts.programmatic_ids_to_jsonschema:write_jsonschema_ids',
                     'import-schema = '
                     'ts_ids_core.scripts.jsonschema_to_programmatic_ids:main_cli']}

setup_kwargs = {
    'name': 'ts-ids-core',
    'version': '0.1.0a2',
    'description': '',
    'long_description': None,
    'author': 'TetraScience',
    'author_email': 'developers@tetrascience.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
