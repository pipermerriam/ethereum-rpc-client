#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

DIR = os.path.dirname(os.path.abspath(__file__))

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

version = '0.4.1'

readme = open(os.path.join(DIR, 'README.md')).read()


setup(
    name='ethereum-rpc-client',
    version=version,
    description="""Ethereum JSON RPC Client""",
    long_description=readme,
    author='Piper Merriam',
    author_email='pipermerriam@gmail.com',
    url='https://github.com/pipermerriam/ethereum-rpc-client',
    include_package_data=True,
    py_modules=['ethereum_rpc_client'],
    install_requires=[
        "requests>=2.7.0",
    ],
    license="MIT",
    zip_safe=False,
    keywords='ethereum json json-rpc',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
