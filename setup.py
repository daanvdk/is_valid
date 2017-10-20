#! /usr/bin/env python3
from setuptools import setup


setup(
    name='is_valid',
    packages=['is_valid'],
    package_dir={'is_valid': 'is_valid'},
    license='MIT',
    version='0.3.0.1',
    description='A small validation library.',
    author='Daan van der Kallen',
    author_email='mail@daanvdk.com',
    url='https://github.com/daanvdk/is_valid',
    keywords=['validation', 'nested'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
    ],
    test_suite='tests',
    tests_require=['hypothesis>=3.21.2'],
)
