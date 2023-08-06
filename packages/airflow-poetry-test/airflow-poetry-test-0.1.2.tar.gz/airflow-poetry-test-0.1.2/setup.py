# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['airflow_poetry_test']

package_data = \
{'': ['*']}

install_requires = \
['airflow-provider-great-expectations>=0.1.4,<0.2.0',
 'apache-airflow-providers-amazon>=3.3.0,<4.0.0',
 'apache-airflow-providers-jira>=2.0.4,<3.0.0',
 'apache-airflow-providers-slack',
 'google-cloud-datastore>=2.5.1,<3.0.0']

setup_kwargs = {
    'name': 'airflow-poetry-test',
    'version': '0.1.2',
    'description': 'Test packages para composer',
    'long_description': None,
    'author': 'Guillermo Britos',
    'author_email': 'guillermo.britos@uala.com.ar',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
