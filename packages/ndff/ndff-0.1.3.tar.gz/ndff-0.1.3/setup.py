# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ndff',
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1.3',
    description='A package to interact with the Dutch NDFF-api',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Richard Duivenvoorde',
    author_email='richard@zuidt.nl',
    url='https://gitlab.com/rduivenvoorde/ndff-connector',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'requests',
        'psycopg2',
        'shapely',
    ],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': ['sphinx'],
        'test': ['pytest'],
    },
)

