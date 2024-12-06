#!/usr/bin/env python
# -*- coding: utf-8 -*-

"Setup for brainmaze-zmq "

from os import path

from setuptools import find_packages, setup

NAME='brainmaze-zmq'
DESCRIPTION='Utils for around zmq supporting multiprocess communication'
EMAIL='mivalt.filip@mayo.edu'
AUTHOR='Filip Mivalt'
VERSION='0.0.1'
REQUIRES_PYTHON = '>=3.9.0'
URL=''
PACKAGES = find_packages()
REQUIRED = []

# if requirements.txt exists, use it to populate the REQUIRED list
if path.exists('./requirements.txt'):
    with open('./requirements.txt') as f:
        REQUIRED = f.read().splitlines()


here = path.abspath(path.dirname(__file__))

print(f'Installing {NAME}')

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    install_requires=REQUIRED,
    packages=PACKAGES,
    python_requires=REQUIRES_PYTHON,
    include_package_data=True,
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: Microsoft :: Windows'
    ],

)
