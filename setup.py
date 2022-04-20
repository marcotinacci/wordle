#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages


setup(
    author="Marco Tinacci",
    author_email='tinacci.marco@gmail.com',
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'wordle=wordle.cli:main',
        ],
    },
    license="MIT license",
    keywords='worlde',
    name='wordle',
    description='Wordle game',
    packages=find_packages(include=['wordle', 'wordle.*']),
    test_suite='tests',
    url='https://github.com/marcotinacci/wordle',
    version='0.5.0',
)
