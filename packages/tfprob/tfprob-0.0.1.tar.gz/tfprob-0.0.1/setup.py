#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from setuptools import find_packages, setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tfprob'))
from version import __version__ as version

setup(
    name='tfprob',
    version=version,
    description='tfprob',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Google Inc.',
    author_email='packages@tensorflow.org',
    url='http://github.com/tensorflow/probability/',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
    ],
)
