#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'data_preparation',
    version = '1.0',
    packages = find_packages(),
    entry_points =  {'scrapy': ['settings = steam.settings']},
    install_requires=[
        'scrapy',
        'smart_getenv',
        'botocore'
    ]
)