#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='yggdrasil_shared',
    version='0.0.28',
    description='Yggdrasil Shared library',
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=True,
    install_requires=[
        'sqlalchemy~=1.4.0',
        'nameko>=3.0.0',
        'marshmallow==3.6.0',
        'walrus~=0.8.0',
        'boto3==1.18.11',
    ],
    extras_require={
        'dev': [
            'pytest~=6.2.0',
            'coverage~=5.5.0',
            'flake8~=3.9.0',
        ],
    },
)
