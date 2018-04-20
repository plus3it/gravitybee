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
@click.option('--setup-file', '-f', 'setup_file', default='setup.cfg',
              help='Name of the setup file to process.')
@click.option('--platform', '-p', 'platform', default=None,
              help='Defaults to the current machine, use this option \
              to override (e.g., Windows or Linux).')
@click.option('--verbose', '-v', 'verbose', is_flag=True,
              help='Displays extra information about processing.')
@click.option('--auto-load', '-a', 'auto_load', is_flag=True,
              help='Install, if necessary, and import all required \
              packages.')
@click.option('--display', '-d', 'display', is_flag=True,
              help='Display package information but do not install or \
              import packages.')

def main(**kwargs):
    """Entry point for GravityBee CLI."""

    print("GravityBee CLI,", gravitybee.__version__)

    # Remove unused options
    empty_keys = [k for k,v in kwargs.items() if not v]
    for k in empty_keys:
        del kwargs[k]

    exit_val = 0

    # Create an instance
    p = gravitybee.ConfigRep(**kwargs)

    if kwargs.get('display',False):
        if not (p.read_config() and p.load_config()):
            exit_val = 1

    elif kwargs.get('auto_load',False):
        if not p.process_config():
            exit_val = 1

    sys.exit(exit_val)