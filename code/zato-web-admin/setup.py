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
    name = 'zato-web-admin',
    version = get_version(),

    author = 'Zato Developers',
    author_email = 'info@zato.io',
    url = 'https://zato.io',

    package_dir = {'':'src'},
    packages = find_packages('src'),

    namespace_packages = ['zato'],
    include_package_data = True,

    install_requires=[
        'django-openid-auth>=0.5',
        'django-settings>=1.3-11',
        'python-openid>=2.2.5',
        'Pygments>=1.6',
    ],
    cmdclass={'version': Version, 'sdist': sdist },
    zip_safe = False,
)
