# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['todo_cli_tddschn']

package_data = \
{'': ['*']}

install_requires = \
['colorama==0.4.4',
 'logging-utils-tddschn>=0.1.5,<0.2.0',
 'shellingham==1.4.0',
 'sqlmodel>=0.0.6,<0.0.7',
 'tabulate>=0.8.9,<0.9.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['todo = todo_cli_tddschn.cli:app']}

setup_kwargs = {
    'name': 'todo-cli-tddschn',
    'version': '0.1.5',
    'description': 'CLI Todo app with typer and sqlite',
    'long_description': None,
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
