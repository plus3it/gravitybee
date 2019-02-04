# -*- coding: utf-8 -*-
"""Utilities for fixing issues with distutils."""

import distutils
from distutils.sysconfig import get_python_lib   # pylint: disable=import-error
import os
import shutil


def _get_real_distutils_path():
    distutils_dir = getattr(distutils, 'distutils_path', None)
    if distutils_dir is None:
        raise NotADirectoryError("Unable to find distutils")
    return os.path.dirname(distutils_dir)


def _get_venv_distutils_parent():
    return os.path.abspath(os.path.join(get_python_lib(), os.pardir))


def _get_venv_distutils_path():
    return os.path.join(_get_venv_distutils_parent(), 'distutils')


def replace_venv_distutils():
    """Replace the fake distutils dir in virtual env with real distutils."""
    shutil.move(
        _get_venv_distutils_path(), _get_venv_distutils_path() + '-moved')
    shutil.copytree(_get_real_distutils_path(), _get_venv_distutils_path())


def unreplace_venv_distutils():
    """Put fake distutils dir back after it has been replaced with real."""
    shutil.rmtree(_get_venv_distutils_path())
    shutil.move(
        _get_venv_distutils_path() + '-moved', _get_venv_distutils_path())
