# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snowbear']

package_data = \
{'': ['*']}

install_requires = \
['PyPika>=0.48.9,<0.49.0',
 'pandas>=1.4.1',
 'pyarrow>=5.0.0',
 'snowflake-connector-python>=2.7.0',
 'snowflake-sqlalchemy>=1.3.0']

setup_kwargs = {
    'name': 'snowbear',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Omri Fima',
    'author_email': 'omrif@diagnosticrobotics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
