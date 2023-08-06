#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-module-docstring,exec-used

import setuptools
from textwrap import dedent

with open('README.md', 'r') as file:
    long_description = file.read()

# DO NOT EDIT THIS NUMBER!
# IT IS AUTOMATICALLY CHANGED BY python-semantic-release
__version__ = "1.0.1"

setuptools.setup(
    name='atom_access',
    version=__version__,
    author='Chilton Group',
    author_email='chilton.group@dummy.com',
    description=dedent(
        'Atom access is a ray tracing package for determining steric \
         hinderance'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent'
        ],
    project_urls={
        "Bug Tracker": "https://gitlab.com/chilton-group/atom_access/-/issues",
        "Documentation": "https://chilton-group.gitlab.io/atom_access/"
    },
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'xyz_py',
        ],
    entry_points={
        'console_scripts': [
            'atom_access = atom_access.cli:main'
            ]
        }
    )
