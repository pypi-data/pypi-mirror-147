#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os

dependency_libs = [
    "mock",
    # https://github.com/ahupp/python-magic
    "python_magic",
    "python_dateutil",
    "pytz",
    "requests",
    "six",
    "tzlocal",
]

script_dir = os.path.dirname(os.path.realpath(__file__))

with open("README.rst", "r") as f:
    readme_text = f.read()

setup(
    name="sornobase",
    version="0.1.1",
    description="Herman Tai's base library for common utilities",
    long_description=readme_text,
    author="Herman Tai",
    author_email="htaihm@gmail.com",
    license="APLv2",
    url="https://github.com/hermantai/sornobase",
    download_url="https://github.com/hermantai/sornobase/archive/master.zip",
    packages=[
        "sornobase",
    ],
    py_modules=[
        "sornobase",
    ],
    requires=dependency_libs,
    install_requires=dependency_libs,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: Apache Software License",
    ],
)
