import io
import re
import os
import sys

from setuptools import setup

long_description = """
## pyco-template

- Fast 
- Simple
- Easy To Use 
- Lightweight (no more requirements)
"""
fp_readme = "readme.md"
if os.path.exists(fp_readme):
    with open(fp_readme, "r") as f:
        long_description = f.read()

setup(
    name='pyco_template',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version="0.0.1",

    description='support json template for python developers',
    long_description=long_description,
    long_description_content_type="text/markdown",

    # The project's main homepage.
    url='http://github.com/dodoru/pyco-template',
    author='dodoru',
    author_email='dodoru@foxmail.com',
    maintainer='dodoru',
    maintainer_email='dodoru@foxmail.com',

    zip_safe=False,
    platforms='any',
    license='GNU LGPLv3',

    # What does your project relate to?
    keywords='Python json template format render',

    install_requires=[],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=[
        'pyco_template',
    ],

    include_package_data=True,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[
    ],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
    },

)
