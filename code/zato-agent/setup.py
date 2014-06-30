#!/usr/bin/env python

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
    name = 'zato-agent',
    version = get_version(),
    author = 'Zato Developers',
    author_email = 'info@zato.io',
    url = 'https://zato.io',
    package_dir = {'':'src'},
    packages = find_packages('src'),
    namespace_packages = ['zato'],
    setup_requires=['hgdistver'],
    get_version_from_git=True,
    zip_safe = False,
)
