# -*- coding: utf-8 -*-
"""gravitybee module.

This module helps in generating standalone applications from python
packages using PyInstaller.

The basic functionality of Gravity Bee was laid out by
Nicholas Chammas (@nchammas) in a project called FlintRock.

Attributes:
    VERB_MESSAGE_PREFIX: A str that is displayed before verbose
        messages.
    verbose: A bool representing whether verbose mode is on.
    pyppy: An instance of pyppyn.ConfigRep for gathering application
        information.
    verboseprint: A function that prints verbose messages if in
        verbose mode.

Example:
    Help using the gravitybee CLI can be found by typing the following::

        $ gravitybee --help
"""

import sys
import os
import pyppyn
import gravitybee
import platform
import shutil
import subprocess
import uuid
import glob
import json
from string import Template

import sys # won't need if no system.exit

__version__ = "0.1.10"
VERB_MESSAGE_PREFIX = "[GravityBee]"
EXIT_OKAY = 0

verbose = False
pyppy = None
verboseprint = lambda *a, **k: \
    print(gravitybee.VERB_MESSAGE_PREFIX, *a, **k) \
    if gravitybee.verbose else lambda *a, **k: None

class Arguments(object):
    """
    A class representing the configuration information needed by the
    gravitybee.PackageGenerator class.

    Attributes:
        clean: A bool indicating whether to clean temporary work from
            the build when complete.
        pkg_dir: A str with location of setup.py for the package to
            be built into a standalone application.
        src_dir: A str with relative path of directory with the
            package source code (e.g., src)
        name_format: A str that represents the format to be used in
            naming the standalone application.
        extra_data: A list of str providing any extra data that
            should be included with the standalone application.
        work_dir: A str with a relative path of directory to be used
            by GravityBee for work files.
        console_script: A str of the name of the first console script
            listed in setup.py or setup.cfg.
        app_version: A str of the version of the standalone
            application pulled from setup.py or setup.cfg.
        app_name: A str with name of the application (which is not
            the same as the file name) to be built.
        pkg_name: A str of the name of the package containing the
            application that will be built.
        script_path: A str of the path the script installed by pip
            when the application is installed.
    """

    def __init__(self, *args, **kwargs):
        """Instantiation"""

        # Remove unused options
        empty_keys = [k for k,v in kwargs.items() if not v]
        for k in empty_keys:
            del kwargs[k]

        # arguments that do NOT depend on pyppyn
        gravitybee.verbose = kwargs.get('verbose',False)
        self.clean = kwargs.get('clean',False)

        self.pkg_dir = kwargs.get(
            'pkg_dir',
            os.environ.get(
                'GB_PKG_DIR',
                '.'
            )
        )

        self.src_dir = kwargs.get(
            'src_dir',
            os.environ.get(
                'GB_SRC_DIR',
                '.'
            )
        )

        self.name_format = kwargs.get(
            'name_format',
            os.environ.get(
                'GB_NAME_FORMAT',
                '{an}-{v}-standalone-{os}-{m}'
            )
        )

        self.extra_data = kwargs.get(
            'extra_data',
            None
        )

        self.dont_write_file = kwargs.get(
            'no_file',
            False
        )

        self.work_dir = kwargs.get(
            'work_dir',
            os.environ.get(
                'GB_WORK_DIR',
                'gb_workdir_' + uuid.uuid1().hex[:16]
            )
        )

        if os.path.exists(self.work_dir):
            print(
                gravitybee.VERB_MESSAGE_PREFIX,
                "ERROR: work_dir must not exist. It may be deleted."
            )
            raise FileExistsError

        # arguments that DO depend on pyppyn
        gravitybee.pyppy = pyppyn.ConfigRep(setup_path=self.pkg_dir,verbose=gravitybee.verbose)

        self.console_script = gravitybee.pyppy.get_config_attr('console_scripts')
        self.app_version = gravitybee.pyppy.get_config_attr('version')

        # Initial values
        self.app_name = kwargs.get(
            'app_name',
            os.environ.get(
                'GB_APP_NAME',
                gravitybee.pyppy.app_name
            )
        )

        self.pkg_name = kwargs.get(
            'pkg_name',
            os.environ.get(
                'GB_PKG_NAME',
                gravitybee.pyppy.get_config_attr('packages')
            )
        )

        self.script_path = kwargs.get(
            'script_path',
            os.environ.get(
                'GB_SCRIPT',
                self._find_script()
            )
        )

        gravitybee.verboseprint("Arguments:")
        gravitybee.verboseprint("app_name:",self.app_name)
        gravitybee.verboseprint("app_version:",self.app_version)
        gravitybee.verboseprint("console_script:",self.console_script)
        gravitybee.verboseprint("pkg_name:",self.pkg_name)
        gravitybee.verboseprint("script_path:",self.script_path)
        gravitybee.verboseprint("pkg_dir:",self.pkg_dir)
        gravitybee.verboseprint("src_dir:",self.src_dir)
        gravitybee.verboseprint("name_format:",self.name_format)
        gravitybee.verboseprint("clean:",self.clean)
        gravitybee.verboseprint("work_dir:",self.work_dir)

        if self.extra_data is not None:
            for extra_data in self.extra_data:
                gravitybee.verboseprint("extra_data:",extra_data)

    def _find_script(self):

        # Windows example: C:\venv\Scripts\<console-script>-script.py

        possible_paths = []

        # likely posix
        possible_paths.append(os.path.join(
            os.environ.get('VIRTUAL_ENV'),
            'bin',
            self.console_script
        ))

        # likely windows
        possible_paths.append(os.path.join(
            os.environ.get('VIRTUAL_ENV'),
            'Scripts',
            self.console_script + '-script.py'
        ))

        # other windows
        possible_paths.append(os.path.join(
            os.environ.get('VIRTUAL_ENV'),
            'Scripts',
            self.console_script + '.py'
        ))

        # unlikely posix
        possible_paths.append(os.path.join(
            os.environ.get('VIRTUAL_ENV'),
            'bin',
            self.console_script + '-script.py'
        ))

        # without virtual env dir
        possible_paths.append(os.path.join(
            'bin',
            self.console_script
        ))

        possible_paths.append(os.path.join(
            'bin',
            self.console_script + '-script.py'
        ))

        possible_paths.append(os.path.join(
            'Scripts',
            self.console_script + '-script.py'
        ))
        
        possible_paths.append(os.path.join(
            'Scripts',
            self.console_script
        ))

        for path in possible_paths:
            if os.path.exists(path):
                return path

class PackageGenerator(object):
    """
    Utility for generating standalone executable versions of python
    programs that are already packaged in a standard setuptools
    package.

    Attributes:
        args: An instance of gravitybee.Arguments containing
            the configuration information for GravityBee.
        operating_system: A str of the os. This is automatically
            determined.
        machine_type: A str of the machine (e.g., x86_64)
        standalone_name: A str that will be the name of the
            standalone application.
        gb_dir: A str of the GravityBee runtime package directory.
        gb_filename: A str of the runtime filename.
        created_file: A str with name of file of the standalone
            application created.
        created_path: A str with absolute path and name of file of
            the standalone application created.        
    """

    def __init__(self, args=None):

        self.args = args

        self.created_file = None    # not set until file is created
        self.created_path = None    # not set until file is created

        pl_sys = platform.system().lower()
        self.operating_system = pl_sys if pl_sys != 'darwin' else 'osx'

        self.machine_type = platform.machine().lower()

        self.standalone_name = self.args.name_format.format(
            an=self.args.app_name,
            v=self.args.app_version,
            os=self.operating_system,
            m=self.machine_type)

        self.gb_dir, self.gb_filename = os.path.split(__file__)

        if not os.path.exists(self.args.work_dir):
            os.makedirs(self.args.work_dir)

        self._temp_script = os.path.join(
            self.args.work_dir,
            uuid.uuid1().hex[:16] + '_' + self.args.console_script + '.py')

        gravitybee.verboseprint("Package generator:")
        gravitybee.verboseprint("operating_system:",self.operating_system)
        gravitybee.verboseprint("machine_type:",self.machine_type)
        gravitybee.verboseprint("standalone_name:",self.standalone_name)


    def _create_hook(self):
        # get the hook ready
        template = Template(open(os.path.join(self.gb_dir, "hook-template"), "r").read())

        hook = template.safe_substitute({ 'app_name': self.args.app_name })

        # 1 extra data
        hook += "# collection extra data, if any (using --extra-data option)"
        try:
            for data in self.args.extra_data:
                #datas.append(('../src/watchmaker/static', './watchmaker/static'))
                hook += "\ndatas.append(('"
                hook += self.args.pkg_dir + os.sep
                if self.args.src_dir != '.':
                    hook += self.args.src_dir + os.sep
                hook += self.args.pkg_name + os.sep + data
                hook += "', '" + self.args.pkg_name + "/" + data + "'))"
                hook += "\n\n"
        except:
            pass

        # 2 package metadata
        hook += "# add dependency metadata"
        for package in gravitybee.pyppy.get_required():
            #datas += copy_metadata(pkg)
            hook += "\ndatas += copy_metadata('" + package + "')"
        hook += "\n"

        # 3 write file
        self.hook_file = os.path.join(self.args.work_dir, "hook-" + self.args.pkg_name + ".py")
        f = open(self.hook_file,"w+")
        f.write(hook)
        f.close()

        gravitybee.verboseprint("Created hook file:",self.hook_file)

    def _cleanup(self):
        # set self.created_file ad self.created_path even if not deleting
        for standalone in glob.glob(os.path.join(self.args.work_dir, 'dist', self.standalone_name + '*')):
            self.created_path = standalone
            self.created_file = os.path.basename(self.created_path)
            gravitybee.verboseprint("Filename:", self.created_file)

        if self.args.clean:
            gravitybee.verboseprint("Cleaning up...")

            # clean work dir
            # get standalone app out first if it exists
            gravitybee.verboseprint("Moving standalone application to current directory:")
            if os.path.exists(os.path.join(os.getcwd(), self.created_file)):
                gravitybee.verboseprint("File already exists, removing...")
                os.remove(os.path.join(os.getcwd(), self.created_file))
            shutil.move(self.created_path, os.getcwd())

            # new path for app now it's been copied
            self.created_path = os.path.join(os.getcwd(), self.created_file)

            if os.path.isdir(self.args.work_dir):
                gravitybee.verboseprint("Deleting working dir:", self.args.work_dir)
                shutil.rmtree(self.args.work_dir)

        gravitybee.verboseprint("Path of standalone:", self.created_path)

    def _write_info_files(self):

        if not self.args.dont_write_file:
            # create memory structure
            gb_files = []
            gb_file = {}
            gb_file['filename'] = self.created_file
            gb_file['path'] = self.created_path
            if self.created_file.endswith(".exe"):
                gb_file['mime-type'] = 'application/vnd.microsoft.portable-executable'
            else:
                gb_file['mime-type'] = 'application/x-executable'
            gb_file['label'] = \
                self.args.app_name \
                + " Standalone Executable (" \
                + self.created_file \
                + ") [GravityBee Build]"
            gb_files.append(gb_file)

            # write to disk
            file_file = open('gravitybee-files.json','w')
            file_file.write(json.dumps(gb_files))
            file_file.close()

            # write all the general info about run for consumption
            # by other apps
            gb_info = {}
            gb_info['app_name'] = self.args.app_name
            gb_info['app_version'] = self.args.app_version
            gb_info['console_script'] = self.args.console_script
            gb_info['script_path'] = self.args.script_path
            gb_info['pkg_dir'] = self.args.pkg_dir
            gb_info['src_dir'] = self.args.src_dir
            gb_info['name_format'] = self.args.name_format
            gb_info['clean'] = self.args.clean
            gb_info['work_dir'] = self.args.work_dir
            gb_info['created_file'] = self.created_file
            gb_info['created_path'] = self.created_path
            gb_info['extra_data'] = []

            if self.args.extra_data is not None:
                for extra_data in self.args.extra_data:
                    gb_info['extra_data'].append(extra_data)
            
            info_file = open('gravitybee-info.json','w')
            info_file.write(json.dumps(gb_info))
            info_file.close()

            del gb_info['extra_data']

            shell = open(
                "gravitybee-environs.sh", 
                mode = 'w',
                encoding = 'utf-8'
            )
            for k, v in gb_info.items():
                shell.write("export ")
                shell.write("GB_" + k.upper())
                shell.write('="')
                shell.write(str(v))
                shell.write('"\n')
            shell.close()

            bat = open(
                "gravitybee-environs.bat", 
                mode = 'w',
                encoding = 'cp1252'
            )
            for k, v in gb_info.items():
                bat.write("set ")
                bat.write("GB_" + k.upper())
                bat.write("=")
                bat.write(str(v))
                bat.write("\r\n")
            bat.close()

    def generate(self):
        self._create_hook()

        try:
            shutil.copy2(self.args.script_path, self._temp_script)
        except FileNotFoundError:
            print(
                gravitybee.VERB_MESSAGE_PREFIX,
                "ERROR: GravityBee could not find your application's " +
                "script in the virtual env that was installed by pip. " +
                "Possible solutions:\n1. Run GravityBee in a virtual " +
                "env;\n2. Point GravityBee to the script using the " +
                "--script option;\n3. Install your application using " +
                "pip;\n4. Make sure your application has a console " +
                "script entry in setup.py or setup.cfg."
            )
            self._cleanup()
            return False

        commands = [
            'pyinstaller',
            '--noconfirm',
            #'--clean',
            '--onefile',
            '--name', self.standalone_name,
            '--paths', self.args.src_dir,
            '--additional-hooks-dir', self.args.work_dir,
            '--specpath', self.args.work_dir,
            '--workpath', os.path.join(self.args.work_dir, 'build'),
            '--distpath', os.path.join(self.args.work_dir, 'dist'),
            '--hidden-import', self.args.pkg_name,
            # This hidden import is introduced by botocore.
            # We won't need this when this issue is resolved:
            # https://github.com/pyinstaller/pyinstaller/issues/1844
            '--hidden-import', 'html.parser',
            # This hidden import is also introduced by botocore.
            # It appears to be related to this issue:
            # https://github.com/pyinstaller/pyinstaller/issues/1935
            '--hidden-import', 'configparser',
            #'--hidden-import', 'packaging', # was required by pyinstaller for a while
            #'--hidden-import', 'packaging.specifiers', # was required by pyinstaller for a while
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

        subproc_args = {}
        subproc_args['check'] = True

        if not gravitybee.verbose:
            subproc_args['stdout'] = subprocess.PIPE
            subproc_args['stderr'] = subprocess.PIPE

        result = subprocess.run(
            commands,
            **subproc_args
        )

        # when not verbose, stdout is available here: result.stdout
        # when not verbose, stderr is available here: result.stderr

        self._cleanup()
        self._write_info_files()
        return gravitybee.EXIT_OKAY

