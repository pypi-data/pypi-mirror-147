# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lfnt']

package_data = \
{'': ['*'], 'lfnt': ['static/*', 'templates/*']}

install_requires = \
['Flask>=2.0.3,<3.0.0',
 'GitPython>=3.1.27,<4.0.0',
 'awscli>=1.22.82,<2.0.0',
 'click-configfile>=0.2.3,<0.3.0',
 'click>=8.0.4,<9.0.0',
 'configparser>=5.2.0,<6.0.0',
 'pulumi>=3.27.0,<4.0.0']

entry_points = \
{'console_scripts': ['lfnt = lfnt.cli:lfnt']}

setup_kwargs = {
    'name': 'lfnt',
    'version': '0.1.11',
    'description': 'For eating development-environment elephants.',
    'long_description': "[![PyPI version](https://badge.fury.io/py/lfnt.svg)](https://badge.fury.io/py/lfnt)\n\n# Elephant (lfnt)\n\n`lfnt` eats development environments.\n\n## What??\n\nSetting up a development environment is a lot like eating an elephant—you have to take it one bite at a time.\nWhether you're such a noob that you don't even know what a noob is or you're such a vet that you already have opinions about this project, you know that starting from scratch is daunting.\nMeanwhile, we all keep eating, and re-eating, the same elephant!\n\nIn my humble opinion, that's just stupid.\n\nBut I'm not alone.\nDevelopers are now commonly adding their config files and installation scripts to their own code repos.\nYet even that is still a pain in the ass to manage, especially when it comes down to every little detail.\n\nThat's where `lfnt` comes in useful—it handles all of the grunt-work for you.\n`lfnt` eases the pain of managing your development environment by:\n\n* Maintaining your configuration repository\n* Keeping track of what packages have been installed and how\n* Restoring your whole setup to a new machine from your configuration repository\n* Providing a platform for environment sharing and test-driving others'\n\nSo just install this package and let `lfnt` do the rest!\n\n## How??\n\n`lfnt` is written in Python3, which means that most workstations are already equipped to use it.\nIt allows you to interact with your environment from a command-line and/or visually from a local web app.\nYou can use it to create a new configuration repository or sync with an existing one—and even perform automatic backups.\n\nAll you need to do is start up a terminal and run:\n\n`pip install lfnt`\n\nAfter the installation is complete, run `lfnt` with no arguments for a synopsis.\nFor example:\n\n```\n$ lfnt\nUsage: lfnt [OPTIONS] COMMAND [ARGS]...\n\n  For eating development-environment elephants.\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  browse    Run in a web browser.\n  dump      Take a config dump.\n  eat       Ingest packages and applications.\n  init      Initialize a configuration.\n  poop      Eliminate packages and applications.\n  remember  Save and commit environment.\n```\n",
    'author': 'Dan Swartz',
    'author_email': '2fifty6@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/2fifty6/lfnt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
