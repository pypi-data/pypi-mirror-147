#!/usr/bin/env python

import configparser
import os
from codecs import open

from setuptools import find_packages, setup

# Import the package module code from local directory.
repo_path = os.path.abspath(os.path.dirname(__file__))

packages = find_packages(exclude=("examples",))

# Open requirements files to grab package dependencies
with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

with open("requirements-test.txt") as f:
    tests_require = [line for line in f if "==" in line]

with open("requirements-dev.txt") as f:
    dev_requires = [line for line in f if "==" in line]

# Open README file to attach readme as package description.
with open("README.md", "r", "utf-8") as f:
    readme = f.read()


# with open(os.path.join(repo_path, "gytrash", "__about__.py"), "r", "utf-8") as f:
about = configparser.ConfigParser()
about.read(os.path.join(repo_path, "pyproject.toml"))

setup(
    name=about["default"]["__title__"].strip('"'),
    version=about["default"]["__version__"].strip('"'),
    description=about["default"]["__description__"].strip('"'),
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["default"]["__author__"].strip('"'),
    author_email=about["default"]["__author_email__"].strip('"'),
    url=about["default"]["__url__"].strip('"'),
    packages=packages,
    package_dir={"gytrash": "gytrash"},
    package_data={"": []},
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=install_requires,
    setup_requires=install_requires,
    extras_require={"test": tests_require, "dev": dev_requires},
    license=about["default"]["__license__"].strip('"'),
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    tests_require=tests_require,
    project_urls={"Source": "https://github.com/trejas/gytrash"},
)
