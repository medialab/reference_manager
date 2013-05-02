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

here = os.path.abspath(os.path.dirname(__file__))

README = open(os.path.join(here, 'README.md')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()

version = '0.3'

with open(os.path.join(here, 'requirements.txt')) as requirements_file:
    requirements = requirements_file.read()

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
]

# classifiers : Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers

config = {
    'name': 'referencemanager',
    'version': version,
    'description': 'ReferenceManager description',
    'long_description': README + '\n\n' + NEWS,
    'classifiers': [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities'
    ],
    'keywords': 'reference biblio endnote bibtext mods',
    'author': 'Sciences Po - médialab',
    'author_email': 'medialab@sciences-po.fr',
    'url': 'https://github.com/medialab/reference_manager',
    'download_url': 'https://github.com/medialab/reference_manager',
    'license': 'tbd',
    'packages': find_packages('referencemanager'),
    'package_dir': {'': 'src'},
    'include_package_data': True,
    'zip_safe': False,
    'install_requires': install_requires,
    'packages': ['referencemanager'],
    'scripts': [],
    'entry_points': {
        'console_scripts': ['referencemanager=referencemanager:main']
    }
}

setup(**config)
