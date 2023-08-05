# -*- coding: utf-8 -*-
"""
    :author: Dabai
    :url: samuelbaizg.github.io
    :copyright: © 2018 Dabai <zhgbai@163.com>
    :license: MIT, see LICENSE for more details.
"""
import os
from distutils.cmd import Command
from distutils.command.sdist import sdist

from setuptools import setup, find_packages


"""
bai-toolkit
----------------
Core tools for your application
"""


def load_requirements():
    with open('requirements.txt') as f:
        packages = f.read().strip().split('\n')
        return [pkg for pkg in packages]


setup(
    name="btoolkit",
    description="Basic tools for web application.",
    long_description="It includes exception handler, cache, encrypt, flask extension, etl tools and so on.",
    keywords="Web, Flask, ETL",
    packages=find_packages(exclude=['data', 'tests']),
    install_requires=load_requirements()

)
