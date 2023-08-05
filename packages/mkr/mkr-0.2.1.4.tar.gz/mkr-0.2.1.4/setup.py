#!/usr/bin/env python
# coding:utf-8

from setuptools import find_packages, setup

setup(
name='mkr',
version='0.2.1.4',
description='MicroKernel based on outer framework as it\'s inner core. Use python project as plugin.',
author="Eagle'sBaby",
author_email='2229066748@qq.com',
maintainer="Eagle'sBaby",
maintainer_email='2229066748@qq.com',
packages=find_packages(),
platforms=["all"],
license='Apache Licence 2.0',
classifiers=[
'Programming Language :: Python',
'Programming Language :: Python :: 3',
],
install_requires = ["files3"],
keywords = ["microkernel"],
python_requires='>=3', 
)