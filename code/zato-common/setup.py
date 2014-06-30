# -*- coding: utf-8 -*-

"""
Copyright (C) 2010 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

# flake8: noqa
import inspect, json, os, re, subprocess

from distutils.core import setup, Command
from distutils.command.sdist import sdist as _sdist

from setuptools import find_packages

VERSION_PY = '''
# This file is originally generated from Git information by running 'setup.py
# version'. Distribution tarballs contain a pre-generated copy of this file.

__version__ = '{}.{}.{}.rev-{}'
'''

PACKAGE = 'zato-server'
GIT_PATH = '../../.git'


def update_version_py():
    if not os.path.isdir(GIT_PATH):
        print "This does not appear to be a Git repository."
        return
    try:
        p = subprocess.Popen([
           'git',
           'log',
           '--pretty=format:\'%h\'',
           '-n 1',],
            stdout=subprocess.PIPE)
    except EnvironmentError:
        print('Unable to run git, leaving _version.py alone')
        return

    stdout = p.communicate()[0]

    if p.returncode != 0:
        print('Unable to run git, leaving _version.py alone')

    revision = stdout[1:-1].strip()

    # Evaluate release.json in curdir/../release_info/release.json
    _file = inspect.currentframe().f_code.co_filename
    curdir = os.path.dirname(os.path.abspath(_file))
    release_info_dir = os.path.join(curdir, '../release-info')
    release = json.loads(open(os.path.join(release_info_dir, 'release.json')).read())

    f = open('_version.py', 'w')
    f.write(VERSION_PY.format(release['major'], release['minor'], release['micro'], revision))
    f.close()

    print 'set {}/_version.py to {}.{}.{}.rev-{}'.format(
        PACKAGE,
        release['major'],
        release['minor'],
        release['micro'],
        revision)


def get_version():
    try:
        f = open('_version.py')
    except EnvironmentError:
        return None

    for line in f.readlines():
        mo = re.match("__version__ = '([^']+)'", line)
        if mo:
            ver = mo.group(1)
            return ver
    return None


class Version(Command):
    description = 'Update _version.py from Git repo'
    user_options = []
    boolean_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        update_version_py()
        print('Version is now {}'.format(get_version()))


class sdist(_sdist):
    def run(self):
        update_version_py()
        self.distribution.metadata.version = get_version()
        return _sdist.run(self)


setup(
    name='zato-common',
    version=get_version(),

    author='Zato Developers',
    author_email='info@zato.io',
    url='https://zato.io',
    license='GNU Lesser General Public License v3 (LGPLv3)',
    platforms='OS Independent',
    description=(
        'Constants and utils common across the whole of Zato ESB '
        'and app server (https://zato.io)'),

    package_dir={'': 'src'},
    packages=find_packages('src'),
    scripts = ['bin/zato-py'],
    namespace_packages=['zato'],

    install_requires=[
        'anyjson>=0.3.3',
        'base32-crockford>=0.2.0',
        'boto>=2.29.1',
        'bunch>=1.0.1',
        'bzr>=2.6',
        'configobj>=5.0.5',
        'datadiff>=1.1.5',
        'distutils2>=1.0a4',
        'gevent>=1.0',
        'lxml>=3.3.5',
        'memory-profiler>=0.31',
        'mock>=1.0.1',
        'nose>=1.3.3',
        'Paste>=1.7.5.1',
        'pip>=1.5.2',
        'psutil>=2.1.1',
        'psycopg2>=2.5.3',
        'pycrypto>=2.6.1',
        'pyparsing>=2.0.2',
        'python-butler>=0.92',
        'python-dateutil>=2.2',
        'pytz>=2014.4',
        'pyzmq>=2.2.0.1',
        'pyzmq-static>=2.2',
        'redis>=2.9.1',
        'rsa>=3.1.4',
        'springpython>=1.3.0RC1',
        'texttable>=0.8.1',
        'urllib3>=1.5',
        'WebHelpers>=1.3',
        'zato-redis-paginator',
    ],

    keywords=(
        'soa eai esb middleware messaging queueing asynchronous integration '
        'performance http zeromq framework events agile broker messaging '
        'server jms enterprise python middleware clustering amqp nosql '
        'websphere mq wmq mqseries ibm amqp zmq'),
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
        ('License :: OSI Approved :: GNU Lesser General '
            'Public License v3 (LGPLv3)'),
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: C',
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
        'Topic :: Internet :: File Transfer Protocol (FTP)',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Object Brokering',
    ],
    cmdclass={'version': Version, 'sdist': sdist },
    zip_safe = False,
)
