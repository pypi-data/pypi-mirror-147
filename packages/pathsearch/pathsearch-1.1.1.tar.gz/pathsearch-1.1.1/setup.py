# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pathsearch']
entry_points = \
{'console_scripts': ['pathsearch = pathsearch:real_main']}

setup_kwargs = {
    'name': 'pathsearch',
    'version': '1.1.1',
    'description': 'A script to search for a file in a list of directories.',
    'long_description': ".. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336\n    :target: https://pycqa.github.io/isort/\n    :alt: isort\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: black\n\n.. image:: https://img.shields.io/pypi/v/pathsearch\n    :target: https://pypi.org/project/pathsearch/\n    :alt: pypi version\n\n.. image:: https://img.shields.io/pypi/dm/pathsearch\n    :target: https://pypi.org/project/pathsearch/\n    :alt: downloads/monthly\n\n.. image:: https://static.pepy.tech/badge/pathsearch\n    :target: https://pypi.org/project/pathsearch/\n    :alt: total downloads\n\n.. image:: https://img.shields.io/pypi/pyversions/pathsearch\n    :target: https://pypi.org/project/pathsearch/\n    :alt: python versions\n\n.. image:: https://img.shields.io/pypi/l/pathsearch\n    :target: https://pypi.org/project/pathsearch/\n    :alt: license\n    \npathsearch\n----------\n\nA script to search for a file in a list of directories.\n\nInstall\n=======\n\nYou can install this script from PyPi with your favorite package manager.\nFor example:\n::\n    \n    pip install pathsearch\n    poetry add pathsearch\n\nUsage\n=====\n\n::\n\n    $ pathsearch -h\n    usage: pathsearch [-h] [-V] [-pe] [-v | -q] (-p PATH | -e VAR) file\n\n    Search for a file in a list of directories\n\n    positional arguments:\n    file                  File to search for on the specified path\n\n    options:\n    -h, --help            show this help message and exit\n    -V, --version         show program's version number and exit\n    -pe, --pathext        Look for file with extensions in environment variable PATHEXT (normally only set on Windows) (default: False)\n    -v, --verbose         Be verbose\n    -q, --quiet           Be quiet (only print found files)\n    -p PATH, --path PATH  Literal path to look in (e.g. /usr/bin:/bin:/usr/sbin:/sbin)\n    -e VAR, --env VAR     Environment variable to take path to search from (e.g. PATH or LD_LIBRARY_PATH)\n\nYou can specify a literal path to look in with the ``-p`` or ``--path`` option.\nOr, you can specify an environment variable to take the path from with the ``-e`` or ``--env`` option.\nThe ``-pe`` or ``--pathext`` option is generally only useful on Windows,\nand will look for files with extensions in the PATHEXT environment variable, for example,\n``pathsearch -pe -e PATH cmd`` will look for ``cmd.exe``, ``cmd.bat``, ``cmd.com`` etc. in the path.\nSee `<https://superuser.com/questions/1027078/what-is-the-default-value-of-the-pathext-environment-variable-for-windows>`_ for more information.\n\nLicense\n=======\n\nThis project is licensed under the MIT license.\n",
    'author': 'mrlegohead0x45',
    'author_email': 'mrlegohead0x45@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mrlegohead0x45/pathsearch',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
