#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='ro-check',
    version='0.1',
    packages=find_packages(),
    license='Apache Licence 2',
    description='tool for validating research objects',
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': ['ro-check=rocheck.cli:main'],
    }
)
