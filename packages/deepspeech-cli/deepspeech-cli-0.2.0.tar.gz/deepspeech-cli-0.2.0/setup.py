# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepspeech_cli']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['ds = deepspeech_cli.deepspeech_cli:app']}

setup_kwargs = {
    'name': 'deepspeech-cli',
    'version': '0.2.0',
    'description': '',
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
