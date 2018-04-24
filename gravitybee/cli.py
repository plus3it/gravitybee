# -*- coding: utf-8 -*-
"""gravitybee cli."""
import os
import platform
import sys

import click

import gravitybee

click.disable_unicode_literals_warning = True

@click.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.version_option(version=gravitybee.__version__)
@click.option('--app-name', '-a', 'app_name', default=None,
              help='Name of the Python application.')
@click.option('--pkg-name', '-n', 'pkg_name', default=None,
              help='The package name for the application you are \
              building.')
@click.option('--script', '-s', 'script_path', default=None,
              help='Path to Python application script.')
@click.option('--src-dir', '-d', 'src_dir', default=None,
              help='Source directory for the package.')
@click.option('--pkg-dir', '-p', 'pkg_dir', default=None,
              help='Directory where setup.py for app lives \
              (not for GravityBee).')
@click.option('--verbose', '-v', 'verbose', is_flag=True,
              help='Verbose mode.')

def main(**kwargs):
    """Entry point for GravityBee CLI."""

    print("GravityBee CLI,", gravitybee.__version__)

    exit_val = 0

    # Create an instance
    args = gravitybee.Arguments(**kwargs)

    if kwargs.get('display',False):
        if not (p.read_config() and p.load_config()):
            exit_val = 1

    elif kwargs.get('auto_load',False):
        if not p.process_config():
            exit_val = 1

    sys.exit(exit_val)