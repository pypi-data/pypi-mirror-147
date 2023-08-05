#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='pdcool',
    version='0.1.0',
    keywords='pdcool',
    description='a library for revang developer',
    license='MIT License',
    url='https://github.com/revang/pdcool',
    author='revang',
    author_email='revang.alternative@foxmail.com',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[
        'requests==2.26.0',
        'pymysql==1.0.2',
        'sqlalchemy==1.4.28',
        'pandas==1.3.5'
    ],
)
