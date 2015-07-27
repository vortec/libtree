# -*- coding: utf-8 -*-
#!/usr/bin/env python

try:
    from setuptools import setup, find_packages, Command
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages, Command

import platform
import os
import subprocess
import sys


if platform.python_implementation() == 'PyPy':
    psycopg2_dependency = 'psycopg2cffi==2.7.1'
else:
    psycopg2_dependency = 'psycopg2==2.6.1'


setup(
    name='libtree',
    version='0.0.1',
    author='Fabian Kochem',
    author_email='fabian.kochem@concepts-and-training.de',
    description='Library for high and bulky trees',

    # Dependencies
    install_requires=[
        psycopg2_dependency
    ],

    # Various stuff (do not care about those)
    entry_points={},
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True
)
