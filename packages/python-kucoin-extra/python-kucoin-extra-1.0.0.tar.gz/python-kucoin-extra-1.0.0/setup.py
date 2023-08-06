#!/usr/bin/env python
import codecs
import os
import re
import sys
from setuptools import setup


setup(
    name='python-kucoin-extra',
    version="1.0.0",
    description='Kucoin REST API v2 python implementation',
    url='https://github.com/javadebadi/python-kucoin',
    author='Javad Ebadi',
    license='MIT',
    author_email='',
    install_requires=['requests', 'websockets'],
    keywords='kucoin exchange rest api bitcoin ethereum btc eth kcs',
    classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
