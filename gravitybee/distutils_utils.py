# -*- coding: utf-8 -*-
"""Utilities for fixing issues with distutils.

In a virtual env, distutils is not an actual package but a skeleton pointing
to the non-virtual Python install distutils. The pyinstaller distutils hook is
supposed to handle this issue and ensure that the real distutils is included
with standalone packages. However, the hook has not been working and the
maintainers seem uninterested in discussing:
https://github.com/pyinstaller/pyinstaller/issues/4031

This is a workaround.

replace_venv_distutils() copies the real distutils directory into the virtual
env and unreplace_venv_distutils() puts everything back. This can be used in
gravitybee right before building the standalone. If the hook works, these
utilities will have no effect. If the hook doesn't work, it will allow
standalones to still have a valid copy of distutils."""

import distutils
from distutils.sysconfig import get_python_lib   # pylint: disable=import-error
import os
import shutil


DISTUTILS_DIR = getattr(distutils, 'distutils_path', None)


def _get_real_distutils_path():
    if DISTUTILS_DIR is None:
        raise NotADirectoryError("Unable to find distutils")
    return os.path.dirname(DISTUTILS_DIR)


def _get_venv_distutils_parent():
    return os.path.abspath(os.path.join(get_python_lib(), os.pardir))


def _get_venv_distutils_path():
    return os.path.join(_get_venv_distutils_parent(), 'distutils')


def fix_distutils():
    """Attempt to fix issues with distutils"""
    if DISTUTILS_DIR and DISTUTILS_DIR.endswith('__init__.py'):
        distutils.distutils_path = os.path.dirname(DISTUTILS_DIR)


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
