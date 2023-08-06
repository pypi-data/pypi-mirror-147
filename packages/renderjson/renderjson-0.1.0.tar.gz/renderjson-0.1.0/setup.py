# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['renderjson']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.1,<4.0.0', 'hvac>=0.11.2,<0.12.0', 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['renderjson = renderjson.main:app']}

setup_kwargs = {
    'name': 'renderjson',
    'version': '0.1.0',
    'description': 'CLI to render Jinja2 template.  There are almost certainly many like it, but this one is mine!',
    'long_description': None,
    'author': 'Jackson Gilman',
    'author_email': 'jackson.j.gilman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
