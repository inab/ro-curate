#!/usr/bin/env python

import os
from setuptools import setup, find_packages
from rocurate import VERSION


def read_file(path):
    return open(os.path.join(os.path.dirname(__file__), path)).read()


setup(
    name='ro-curate',
    version=VERSION,
    packages=find_packages(),
    license='Apache Licence 2',
    description='tool for validating and refining research objects',
    long_description=read_file('README.md'),
    entry_points={
        'console_scripts': ['rocurate=rocurate.cli:main'],
    },
    package_data={
        'rocurate.shapes': ['shapes.ttl']
    },
)
