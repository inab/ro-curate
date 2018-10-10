#!/usr/bin/env python

import os
from setuptools import setup, find_packages
from rocheck import VERSION


def read_file(path):
    return open(os.path.join(os.path.dirname(__file__), path)).read()


setup(
    name='ro-check',
    version=VERSION,
    packages=find_packages(),
    license='Apache Licence 2',
    description='tool for validating research objects',
    long_description=read_file('README.md'),
    entry_points={
        'console_scripts': ['ro-check=rocheck.cli:main'],
    }
)
