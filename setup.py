#!/usr/bin/env python

import os

from setuptools import setup


long_description = ""
if os.path.isfile("README.rst"):
    long_description = open("README.rst", "r", encoding="UTF-8").read()


setup(
    name="scanline-python-wrapper",
    version="1.0.0",
    description="Python wrapper for the scanline CLI scanner tool for macOS",
    license="BSD 3 Clause",
    long_description=long_description,
    author="Wanadev <contact@wanadev.fr>",
    py_modules=["scanline_wrapper"],
    include_package_data=True,
    install_requires=[],
    extras_require={
        "dev": [
            "nox",
            "flake8",
            "black",
            "pytest",
            "sphinx",
            "sphinx-rtd-theme",
        ]
    },
)
