#!/usr/bin/env python

from setuptools import setup, find_packages
from rocheck import VERSION

setup(
    name='ro-check',
    version=VERSION,
    packages=find_packages(),
    license='Apache Licence 2',
    description='tool for validating research objects',
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': ['ro-check=rocheck.cli:main'],
    }
)
