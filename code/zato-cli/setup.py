# -*- coding: utf-8 -*-

"""
Copyright (C) 2010 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

# flake8: noqa
from distutils.core import setup
from hgdistver import get_version
from setuptools import find_packages


DESC = 'Convenience Python client for Zato ESB and app server (https://zato.io)'


setup(
    name = 'zato-cli',
    version = get_version(),

    author = 'Zato Developers',
    author_email = 'info@zato.io',
    url = 'https://zato.io',

    package_dir = {'':'src'},
    packages = find_packages('src'),

    namespace_packages = ['zato'],
    install_requires = [
        'Importing>=1.10',
        'Django>=1.6.5',
        'pg8000>=1.9.10',
        'pyaml>=14.05.7',
        'sarge>=0.1.3',
        'SQLAlchemy>=0.7.4',
    ],
    setup_requires=['hgdistver'],
    get_version_from_git=True,
    zip_safe = False,
    entry_points = """
        [console_scripts]
        zato = zato.cli.zato_command:main
    """
)
