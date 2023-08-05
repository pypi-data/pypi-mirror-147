# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['todo_cli_typer']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.35,<2.0.0',
 'colorama==0.4.4',
 'shellingham==1.4.0',
 'tabulate>=0.8.9,<0.9.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['todo = todo_cli_typer.__main__:main']}

setup_kwargs = {
    'name': 'todo-cli-typer',
    'version': '0.6.0',
    'description': 'CLI Todo app with typer, FastAPI and sqlite',
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
