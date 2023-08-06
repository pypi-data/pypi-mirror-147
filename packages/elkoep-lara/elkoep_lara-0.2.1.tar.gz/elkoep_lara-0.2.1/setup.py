#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import warnings

from setuptools import setup, find_packages

version = '0.2.1'

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='elkoep_lara',
    version=version,
    author='Vyacheslav Anisimov',
    author_email='kajfash@lycos.com',
    url='https://github.com/exKAjFASH/',
    packages=find_packages(),
    scripts=[],
    description='Python API for controlling ElkoEP Lara devices',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    include_package_data=True,
    zip_safe=False,
)
