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
              help='Path to Python application script installed by pip in the virtual env.')
@click.option('--src-dir', '-d', 'src_dir', default=None,
              help='Source directory for the package.')
@click.option('--pkg-dir', '-p', 'pkg_dir', default=None,
              help='Directory where setup.py for app lives \
              (not for GravityBee).')
@click.option('--verbose', '-v', 'verbose', is_flag=True,
              help='Verbose mode.')
@click.option('--extra-data', '-e', 'extra_data', multiple=True,
              help='Any extra data to be included with the \
              standalone application. Can me used multiple times.')
@click.option('--work-dir', '-w', 'work_dir', default=None,
              help='Relative path for work directory.')
@click.option('--clean', '-c', 'clean', is_flag=True,
              help='Whether or not to clean up work area. If used, the create standalone application will be placed in the \
              directory where GravityBee is run. Otherwise, it is placed in the work_dir.')    
@click.option('--name-format', '-f', 'name_format', default=None,
              help='Format to be used in naming the standalone application. Must include {an}, {v}, {os}, {m} \
              for app name, version, os, and machine type respectively.') 
@click.option('--no-file', 'no_file', is_flag=True, default=False,
              help='Do not write gravitybee-files.json file with name of standalone.')                           

def main(**kwargs):
    """Entry point for GravityBee CLI."""

    print("GravityBee CLI,", gravitybee.__version__)

    # Create an instance
    args = gravitybee.Arguments(**kwargs)
    pg = gravitybee.PackageGenerator(args)
    sys.exit(pg.generate())