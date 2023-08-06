#!/usr/bin/env python
import codecs
import os
import re
import sys
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def install_requires():

    requires = ['requests']
    if sys.version_info > (3, 4):
        requires.extend(['websockets'])
    return requires


setup(
    name='python-kucoin-xx',
    version="1.2.0",
    description='Kucoin REST API v2 python implementation',
    url='https://github.com/javadebadi/python-kucoin',
    author='Javad Ebadi',
    license='MIT',
    author_email='',
    install_requires=install_requires(),
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
