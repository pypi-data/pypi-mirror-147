# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbtenv_dbt_alias']

package_data = \
{'': ['*']}

install_requires = \
['dbtenv==2.2.1']

entry_points = \
{'console_scripts': ['dbt = dbtenv.main:main', 'dbtenv = dbtenv.main:main']}

setup_kwargs = {
    'name': 'dbtenv-dbt-alias',
    'version': '2.2.1',
    'description': "dbtenv, but additionally installs a 'dbt' executable that is functionally equivalent to aliasing the dbt command to 'dbtenv execute --'.",
    'long_description': "# dbtenv-dbt-alias\n\ndbtenv, but additionally installs a 'dbt' executable that is functionally equivalent to aliasing the dbt command to 'dbtenv execute --'.\n",
    'author': 'Brooklyn Data Co.',
    'author_email': 'hello@brooklyndata.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brooklyn-data/dbtenv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
