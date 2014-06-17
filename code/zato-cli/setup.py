# -*- coding: utf-8 -*-

"""
Copyright (C) 2010 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

# flake8: noqa

import os
from setuptools import setup, find_packages

curdir = os.path.dirname(os.path.abspath(__file__))
_version_py = os.path.normpath(os.path.join(curdir, '..', '.version.py'))
_locals = {}
execfile(_version_py, _locals)
version = _locals['version']

setup(
    name = 'zato-cli',
    version = version,

    author = 'Zato Developers',
    author_email = 'info@zato.io',
    url = 'https://zato.io',

    package_dir = {'':'src'},
    packages = find_packages('src'),

    namespace_packages = ['zato'],
    install_requires = [
        'Importing>=1.10',
        'Django>=1.6.5',
        'pyaml>=14.05.7',
        'sarge>=0.1.3',
        'SQLAlchemy>=0.7.4',
    ],

    zip_safe = False,
    entry_points = """
        [console_scripts]
        zato = zato.cli.zato_command:main
    """
)
