#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'ReferenceManager',
    'author': 'Sciences Po - médialab',
    'url': 'https://github.com/medialab/reference_manager',
    'download_url': 'https://github.com/medialab/reference_manager',
    'author_email': '',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['ReferenceManager'],
    'scripts': [],
    'name': 'ReferenceManager'
}

setup(**config)
