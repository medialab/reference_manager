#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    from distutils.core import setup
import sys
import os

import biblib
from biblib.util import constants

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'requirements.txt')) as requirements_file,
            open(os.path.join(here, 'README.md')) as README_file, 
            open(os.path.join(here, 'NEWS.txt')) as NEWS_file, 
            open(os.path.join(here, 'LICENSE')) as LICENSE_file:

    requirements = requirements_file.read().splitlines()
    README = README_file.read()
    NEWS = NEWS_file.read()
    LICENSE = LICENSE_file.read()

    setup(
        name='biblib',
        version=constants.BIBLIB_VERSION,
        author='Sciences Po - médialab',
        author_email='medialab@sciences-po.fr',
        url='https://github.com/medialab/reference_manager',
        download_url='https://github.com/medialab/reference_manager',
        description='biblib description',
        long_description=README + '\n\n' + NEWS,
        include_package_data=True,
        packages=find_packages('biblib'),
        #packages=['biblib'],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Environment :: Web Environment',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Developers',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Programming Language :: Python :: 2.7',
            'Topic :: Utilities'
        ],
        keywords='bibliographic reference endnote bibtext mods',
        license=LICENSE,
        install_requires=requirements,
        entry_points={
            'console_scripts': ['biblib=biblib:main']
        }
    )
