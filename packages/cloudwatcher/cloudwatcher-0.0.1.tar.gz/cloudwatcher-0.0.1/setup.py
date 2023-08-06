#! /usr/bin/env python

import os
from setuptools import setup
import sys

PACKAGE = "cloudwatcher"

# Additional keyword arguments for setup().
extra = {}

# Ordinary dependencies
DEPENDENCIES = []
with open("requirements/requirements-all.txt", "r") as reqs_file:
    for line in reqs_file:
        if not line.strip():
            continue
        DEPENDENCIES.append(line)

extra["install_requires"] = DEPENDENCIES

with open("{}/_version.py".format(PACKAGE), 'r') as versionfile:
    version = versionfile.readline().split()[-1].strip("\"'\n")

# Handle the pypi README formatting.
try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError, OSError):
    long_description = open('README.md').read()

setup(
    name=PACKAGE,
    packages=[PACKAGE],
    version=version,
    description="A tool for monitoring AWS CloudWatch metrics",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: System :: Distributed Computing"
    ],
    keywords="",
    author=u"Michal Stolarczyk",
    author_email=u"michal.stolarczyk@nih.gov", 
    license="BSD2",
    entry_points={
        "console_scripts": [
            'cloudwatcher = cloudwatcher.cloudwatcher:main'
        ],
    },    
    package_data={"cloudwatcher": [os.path.join("cloudwatcher", "*")]},
    include_package_data=True,
    test_suite="tests",
    tests_require=(["pytest"]),
    setup_requires=(["pytest-runner"] if {"test", "pytest", "ptr"} & set(sys.argv) else []),
    **extra
)
