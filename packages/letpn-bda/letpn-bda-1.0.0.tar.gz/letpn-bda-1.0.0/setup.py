# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['letpn_bda']

package_data = \
{'': ['*'], 'letpn_bda': ['db/*', 'raw_text/*']}

install_requires = \
['typer[all]>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['bda-quiz = letpn_bda.main:app']}

setup_kwargs = {
    'name': 'letpn-bda',
    'version': '1.0.0',
    'description': 'This is a Simple Quiz app for Practicing',
    'long_description': '# This is a small typer quiz project\n---\n\n> ### this is created to practice quiz for exam only\n',
    'author': 'PRITAM CHAKRABORTY',
    'author_email': 'pritam.chk98@gmail.com',
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
