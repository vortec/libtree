# Copyright (c) 2015 Fabian Kochem


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

from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


if platform.python_implementation() == 'PyPy':
    psycopg2_dependency = 'psycopg2cffi==2.7.2'
else:
    psycopg2_dependency = 'psycopg2==2.6.1'


setup(
    name='libtree',
    version='2.1.2',
    author='Fabian Kochem',
    author_email='fabian.kochem@concepts-and-training.de',
    description='Python Tree Library',
    url='https://github.com/conceptsandtraining/libtree',

    # Dependencies
    install_requires=[
        psycopg2_dependency
    ],
    tests_require=[
        'pytest',
        'mock'
    ],

    cmdclass={
        'test': PyTest
    },
    entry_points={},
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries'
    ],
)
