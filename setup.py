import os
import re
import sys
import codecs
from os import path
from distutils.sysconfig import get_python_lib
from setuptools import find_packages, setup

# Used later on to net get lost.
here = path.abspath(path.dirname(__file__))

# Get the version from `version`
with codecs.open('version', encoding='utf-8') as vers_file:
    version = vers_file.read().strip()

# Get the long description from the relevant file
with codecs.open('README.rst', encoding='utf-8') as desc_file:
    long_description = desc_file.read()

# Setup function used to define the package meta data
setup(
    # Package name.
    name='serverhud',

    # Package version. either a string like `'1.0.1'` or like this, reading it
    # from the file version in this directory.
    version=version,

    # Source URL of the package.
    url='https://github.com/deadbok/server-hud',

    # Author data.
    author='Martin Bo Kristensen Grønholdt',
    author_email='martin.groenholdt@gmail.com',

    # Description is either a string or, like here, read from the `README.rst`
    # file.
    description=long_description,

    # License
    license='GNU General Public License v2 (GPLv2)',

    # Include the library package.
    packages=['serverhud.app', 'serverhud.ws'],

    scripts=['scripts/serverhud-client', 'scripts/serverhud-server'],

    include_package_data=True,

    # The package requirements.
    install_requires=['Flask', 'tornado', 'watchdog', 'psutil'],

    # We want a version equal to or newer that Python 3.
    python_requires='>=3',

    # Clasifiers for PyPi (not used when installing), look them up at:
    #  https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        'Framework :: Flask',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5'
    ],
)
