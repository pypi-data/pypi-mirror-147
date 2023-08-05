# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hr_tddschn']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['hr = hr_tddschn.hr:cli']}

setup_kwargs = {
    'name': 'hr-tddschn',
    'version': '0.1.8',
    'description': 'Horizontal rule for your terminal - in python3!',
    'long_description': '# hr-tddschn\n\nFork of [hr.py](https://github.com/euangoddard/hr.py), with python3 support.\n\nThe good old [hr](https://github.com/LuRsT/hr) in python3.\n\n- [hr-tddschn](#hr-tddschn)\n  - [Why fork?](#why-fork)\n  - [Intro](#intro)\n  - [Inspiration](#inspiration)\n  - [Install](#install)\n  - [How to use it?](#how-to-use-it)\n    - [From the command-line:](#from-the-command-line)\n    - [From another python script (it could happen, right?)](#from-another-python-script-it-could-happen-right)\n  - [Requirements](#requirements)\n## Why fork?\n\nVersion 0.1 of the original `hr.py` \n(the current latest version of `hr` on [PyPI](https://pypi.org/project/hr/)) doesn\'t work with python3,\n\nthis project adds python3 support and properly configured entry point so that `hr` is added to your `$PATH` after installation.\n\n[Read more](https://github.com/euangoddard/hr.py/issues/3#issuecomment-1100875531)\n\n## Intro\n\nHorizontal rule for your terminal - in python3!\n\nTired of not finding things in your terminal because there\'s a lot of logs and\ngarbage? Tired of destroying the Enter key by creating a "void zone" in your\nterminal so that you can see the error that you\'re trying to debug?\n\nUse the old `<hr />` tag, but in your terminal.\n\n## Inspiration\n\nThe original version of the hr script was implement in bash (https://github.com/LuRsT/hr), and I thought, "why not have a python version?". So here we are!\n\n## Install\n\n```\n$ pip install hr-tddschn\n```\n\nOr, if you only want to use it as a CLI app:\n```\n$ pipx install hr-tddschn\n```\n\nThen run it with `hr`.\n\n## How to use it?\n\n### From the command-line:\n\n    $ hr\n    ################################## # Till the end of your terminal window\n    $\n\n    $ hr \'*\'\n    ********************************** # Till the end of your terminal window\n    $\n\nYou can also make "beautiful" ASCII patterns\n\n    $ hr - \'#\' -\n    ----------------------------------\n    ##################################\n    ----------------------------------\n    $ hr \'-#-\' \'-\' \'-#-\'\n    -#--#--#--#--#--#--#--#--#--#--#--\n    ----------------------------------\n    -#--#--#--#--#--#--#--#--#--#--#--\n\n### From another python script (it could happen, right?)\n\n    >>> from hr_tddschn import hr\n    >>> hr()\n    ################################## # Till the end of your terminal window\n    >>> hr(\'*\')\n    ********************************** # Till the end of your terminal window\n    >>> hr(\'-\', \'#\', \'-\')\n    ----------------------------------\n    ##################################\n    ----------------------------------\n    >>> hr(\'-#-\', \'-\', \'-#-\')\n    -#--#--#--#--#--#--#--#--#--#--#--\n    ----------------------------------\n    -#--#--#--#--#--#--#--#--#--#--#--\n\n## Requirements\n\nThe only requirement is python2.7+ or python3 (tested in python 3.10)\n',
    'author': 'Gonçalves',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=2.7,<4',
}


setup(**setup_kwargs)
