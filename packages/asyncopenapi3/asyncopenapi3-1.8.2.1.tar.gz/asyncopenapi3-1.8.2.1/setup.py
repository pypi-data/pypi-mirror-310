#!/usr/bin/env python3
from __future__ import annotations

import builtins
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))


# get the long description from the README.rst
with builtins.open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="asyncopenapi3",
    version="1.8.2.1",
    description="Async Client and Validator of OpenAPI 3 Specifications",
    long_description=long_description,
    author="smurf@noris.de",
    url="https://github.com/smurfix/openapi3",
    packages=["asyncopenapi3"],
    license="BSD 3-Clause License",
    install_requires=["PyYaml", "httpx"],
    extras_require={
        "test": [
            "pytest==8.3.3",
            "pylint==3.3.1",
            "anyio==4.6.2",
            "hypercorn==0.17.3",
            "pydantic==2.9.2",
            "fastapi==0.110.0",
            "respx==0.21.1",
        ],
    },
)
