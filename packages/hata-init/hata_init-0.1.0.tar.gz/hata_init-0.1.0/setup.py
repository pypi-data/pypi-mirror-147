# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hata', 'hata.main.commands.init']

package_data = \
{'': ['*']}

install_requires = \
['hata>=1.2.8,<2.0.0', 'typer>=0.4.1,<0.5.0']

setup_kwargs = {
    'name': 'hata-init',
    'version': '0.1.0',
    'description': 'A cli plugin for hata which allows you to make bots fast',
    'long_description': None,
    'author': 'WizzyGeek',
    'author_email': '51919967+WizzyGeek@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
