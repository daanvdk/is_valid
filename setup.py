#! /usr/bin/env python3
from setuptools import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='is_valid',
    packages=['is_valid'],
    package_dir={'is_valid': 'is_valid'},
    license='MIT',
    version='0.1.0',
    description='A small validation library.',
    long_description=read('README.md'),
    author='Daan van der Kallen',
    author_email='mail@daanvdk.com',
    url='https://github.com/daanvdk/is_valid',
    keywords=['validation', 'nested'],
    classifiers=[],
    test_suite='tests'
)
