# -*- coding: utf-8 -*-
"""gravitybee setup script."""
from setuptools import setup

import io
import os

if __name__ == "__main__":

    with open('README.rst', 'r') as f:
        long_description = f.read()

    with open('CHANGELOG.rst', 'r') as f:
        long_description += f.read()

    setup(
        long_description=long_description,
    )