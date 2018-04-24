# -*- coding: utf-8 -*-
"""gravitybee module.

This module helps in generating standalone applications from python
packages using PyInstaller.

Example:
    Help using the gravitybee CLI can be found by typing the following::

        $ gravitybee --help
"""

import os
import pyppyn
import gravitybee
import platform
import shutil
import subprocess
import sys
import random
from string import Template

__version__ = "0.1.0"
VERB_MESSAGE_PREFIX = "[GravityBee]"

verbose = False
pyppy = None
verboseprint = lambda *a: print(gravitybee.VERB_MESSAGE_PREFIX, *a) if gravitybee.verbose else lambda *a, **k: None

class Arguments(object):
    """
    Arguments for GravityBee
    """

    app_name = None
    pkg_name = None
    script_path = None
    pkg_dir = None
    src_dir = None
    console_script = None
    app_version = None

    def __init__(self, *args, **kwargs):
        """Instantiation"""

        # Remove unused options
        empty_keys = [k for k,v in kwargs.items() if not v]
        for k in empty_keys:
            del kwargs[k]

        gravitybee.verbose = kwargs.get('verbose',False)
        gravitybee.pyppy = pyppyn.ConfigRep(setup_path=self.pkg_dir,verbose=gravitybee.verbose)

        self.console_script = gravitybee.pyppy.get_config_attr('console_scripts')
        self.app_version = gravitybee.pyppy.get_config_attr('version')

        # Initial values
        self.app_name = kwargs.get(
            'app_name',
            os.environ.get(
                'GB_APP_NAME',
                gravitybee.pyppy.app_name))

        self.pkg_name = kwargs.get(
            'pkg_name',
            os.environ.get(
                'GB_PKG_NAME',
                gravitybee.pyppy.get_config_attr('packages')))

        self.script_path = kwargs.get(
            'script_path',
            os.environ.get(
                'GB_SCRIPT',
                os.path.join(
                    os.environ.get('VIRTUAL_ENV'),
                    'bin',
                    self.console_script)))

        self.pkg_dir = kwargs.get(
            'pkg_dir',
            os.environ.get(
                'GB_PKG_DIR',
                '.'))

        self.src_dir = kwargs.get(
            'src_dir',
            os.environ.get(
                'GB_SRC_DIR',
                'src'))

        self.name_format = kwargs.get(
            'name_format',
            os.environ.get(
                'GB_NAME_FORMAT',
                '{an}-{v}-standalone-{os}-{m}'))

class PackageGenerator(object):
    """
    Utility for generating standalone executable versions of python
    programs that are already packaged in the standard setuptools 
    way.

    Attributes:
        setup_file: A str of the path of the file to process.
        platform: A str of the platform. This is automatically
            determined or can be overriden.
        verbose: A bool of whether to display extra messages.
        config_dict: A dict representing the values in the config
            file.
        python_version: A float with the major and minor versions of
            the currently running python.
        app_version: A str of the version represented by the config
            file.
        this_os_reqs: A list of packages required for this os/env.
        other_reqs: A list of packages that are not required.
            Included for debug so that it is possible to see where
            everything went.
        base_reqs: A list of non-specific requirements that are also
            needed.
        this_python_reqs: A list of packages required for this
            version of python.
    """

    def __init__(self, args=None):
        
        self.args = args
        self.operating_system = platform.system().lower()
        self.machine_type = platform.machine().lower()

        self.standalone_name = self.args.name_format.format(
            an=self.args.app_name,
            v=self.args.app_version,
            os=self.operating_system,
            m=self.machine_type)

        self._temp_script = str(random.randint(10000,99999)) + '_' + self.args.console_script

    def _create_hook(self):
        # get the hook ready
        template = Template("""from PyInstaller.utils.hooks import copy_metadata, collect_data_files, collect_submodules

        hiddenimports = (
            collect_submodules('$app_name}')
        )

        datas = copy_metadata('$app_name}')
        datas += collect_data_files('$app_name}')
        
        """)

        hook = template.safe_substitute({ 'app_name': self.args.app_name })

        # 1 extra data
        for data in self.args.extra_data:
            #datas.append(('../src/watchmaker/static', './watchmaker/static'))
            #hook += "\ndatas.append(('./" + src/watchmaker/static', './watchmaker/static'))"
            pass

        # 2 package metadata
        for package in gravitybee.pyppy.get_required():
            #datas += copy_metadata(pkg)
            hook += "\ndatas += copy_metadata(" + package + ")"

        # 3 write file
        # write hook-pkg_name.py

    def generate(self):
        """
        if self.operating_system.lower() == 'linux':
            src_path = '/var/opt/git/watchmaker/src'
            additional_hooks = '/var/opt/git/gravitybee/pyinstaller'
        elif self.operating_system.lower() == 'windows':
            src_path = 'C:\\git\\watchmaker\\src'
            additional_hooks = 'C:\\git\\gravitybee\\pyinstaller'
        """

        self._create_hook()

        # copy the python script to the current directory
        shutil.copy2(self.args.script_path, os.path.join('.',self._temp_script))

        commands = [
            'pyinstaller',
            '--noconfirm',
            #'--clean',
            '--onefile',
            '--name', self.standalone_name,
            '--paths', self.args.src_path,
            '--additional-hooks-dir', '.',
            '--hidden-import', self.args.pkg_name,
            # This hidden import is introduced by botocore.
            # We won't need this when this issue is resolved:
            # https://github.com/pyinstaller/pyinstaller/issues/1844
            '--hidden-import', 'html.parser',
            # This hidden import is also introduced by botocore.
            # It appears to be related to this issue:
            # https://github.com/pyinstaller/pyinstaller/issues/1935
            '--hidden-import', 'configparser',
            '--hidden-import', 'packaging',
            '--hidden-import', 'packaging.specifiers',
            '--hidden-import', 'pkg_resources',
        ]

        # get all the packages called for by package
        for pkg in gravitybee.pyppy.get_required():
            commands += [
                '--hidden-import', pkg,
            ]

        commands += [
            self._temp_script
        ]

        if self.operating_system != 'windows':
            insert_point = commands.index('--onefile') + 1
            commands[insert_point:insert_point] = ['--runtime-tmpdir', '.']

        gravitybee.verboseprint("PyInstaller commands:")
        gravitybee.verboseprint(*commands, sep=', ')

        subprocess.run(
            commands,
            check=True)

