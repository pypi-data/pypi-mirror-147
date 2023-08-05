# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['run_logger']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'gql>=2.0.0,<3.0.0',
 'jsonlines>=2.0.0,<3.0.0',
 'numpy>=1.19.2,<2.0.0',
 'redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'run-logger',
    'version': '0.1.0',
    'description': 'A utility for logging runs.',
    'long_description': '# Welcome to run-logger\n\nA"run" is a long-running process that depends on a set of parameters and outputs results in the form of logs.\nThis library has three primary functions:\n\n1. Storing run logs in a database.\n2. Storing metadata associated with each run in a database (e.g. for the purposes of reproducibility).\n3. Managing parameters.\n\n# Installation\n\n```bash\npip install run-logger\n``` \n\n# [Documentation](https://run-logger.readthedocs.io/en/latest/index.html)',
    'author': 'Ethan Brooks',
    'author_email': 'ethanabrooks@gmail.com',
    'maintainer': 'Ethan Brooks',
    'maintainer_email': 'ethanabrooks@gmail.com',
    'url': 'https://run-logger.readthedocs.io/en/latest/index.html',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
