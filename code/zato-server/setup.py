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
    name = 'zato-server',
    version = version,

    author = 'Zato Developers',
    author_email = 'info@zato.io',
    url = 'https://zato.io',

    package_dir = {'':'src'},
    packages = find_packages('src'),

    namespace_packages = ['zato'],
    install_requires = [
        'amqp>=1.4.5',
        'arrow>=0.4.2',
        'crontab>=0.20',
        'dpath>=1.2-70',
        'faulthandler>=2.3',
        'fs>=0.5.0',
        'gevent-inotifyx>=0.1.1',
        'globre>=0.1.2',
        'gunicorn>=19.0.0',
        'jsonpointer>=1.3',
        'kombu>=3.0.19',
        'oauth>=1.0.1',
        'paodate>=1.2',
        'parse>=1.6.4',
        'pesto>=25',
        'pika>=0.9.13',
        'psycogreen>=1.0',
        'python-swiftclient>=2.1.0',
        'repoze.profile>=2.0',
        'retools>=0.4.1',
        'scipy>=0.14.0',
        'sec-wall>=1.2',
        'tzlocal>=1.1.1',
        'xmltodict>=0.9.0',
    ],

    zip_safe = False,
)
