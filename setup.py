# Copyright (c) 2015 CaT Concepts and Training GmbH


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
    version='0.0.2',
    author='Fabian Kochem',
    author_email='fabian.kochem@concepts-and-training.de',
    description='Postgres-based library to handle and persist wide trees',

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
