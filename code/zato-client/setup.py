# -*- coding: utf-8 -*-

"""
Copyright (C) 2013 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

# flake8: noqa
from distutils.core import setup
from hgdistver import get_version
from setuptools import find_packages


DESC = 'Convenience Python client for Zato ESB and app server (https://zato.io)'


setup(
    name = 'zato-client',
    version = get_version(),

    author = 'Zato Developers',
    author_email = 'info@zato.io',
    url = 'https://zato.io',
    license = 'GNU Lesser General Public License v3 (LGPLv3)',
    platforms = 'OS Independent',
    description = DESC,
    long_description = DESC,

    package_dir = {'':'src'},
    packages = find_packages('src'),
    namespace_packages = ['zato'],
      
    install_requires=[
        'anyjson>=0.3.3',
        'bunch>=1.0.1',
        'lxml>=3.3.5',
        'requests>=2.3.0',
        'zato-common >=2.0.dev0,<2.1'
    ],
    keywords=('soa eai esb middleware messaging queueing asynchronous integration performance http zeromq framework events agile broker messaging server jms enterprise python middleware clustering amqp nosql websphere mq wmq mqseries ibm amqp zmq'),
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Framework :: Buildout',
        'Intended Audience :: Customer Service',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: C',
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: 2.7',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Communications',
        'Topic :: Database',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
        'Topic :: Internet :: File Transfer Protocol (FTP)',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Object Brokering',
    ],
    setup_requires=['hgdistver'],
    get_version_from_git=True,
    zip_safe = False,
)
