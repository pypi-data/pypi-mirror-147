# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_ml_utils',
 'data_ml_utils.client_boto3',
 'data_ml_utils.core',
 'data_ml_utils.pyathena_client']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==5.4.1',
 'appdirs==1.4.4',
 'attrs==20.3.0',
 'black>=22.3.0,<23.0.0',
 'cfgv==3.2.0',
 'coverage==5.4',
 'distlib==0.3.1',
 'filelock==3.0.12',
 'flake8>=4.0.1,<5.0.0',
 'identify==1.5.13',
 'iniconfig==1.1.1',
 'isort>=5.10.1,<6.0.0',
 'mccabe==0.6.1',
 'mock>=4.0.3,<5.0.0',
 'moto>=3.1.5,<4.0.0',
 'mypy-extensions==0.4.3',
 'nodeenv==1.5.0',
 'packaging==20.9',
 'pandas==1.3.5',
 'pluggy==0.13.1',
 'poetry==1.1.11',
 'pre-commit==2.10.0',
 'py==1.10.0',
 'pyathena>=2.5.2,<3.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'pyparsing==2.4.7',
 'pytest-cov>=3.0.0,<4.0.0',
 'pytest-custom-exit-code==0.3.0',
 'pytest>=7.1.1,<8.0.0',
 'regex==2020.11.13',
 'six==1.15.0',
 'toml==0.10.2',
 'typed-ast==1.4.2',
 'typing-extensions>=4.2.0,<5.0.0',
 'virtualenv==20.4.2']

setup_kwargs = {
    'name': 'data-ml-utils',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Shu Ming Peh',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
