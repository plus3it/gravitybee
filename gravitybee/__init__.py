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
import hashlib

__version__ = "0.1.16"
VERB_MESSAGE_PREFIX = "[GravityBee]"
EXIT_OKAY = 0
FILE_DIR = ".gravitybee"

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

    OPTION_SHA_INFO = "info"
    OPTION_SHA_FILE = "file"

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

        self.sha_format = kwargs.get(
            'sha_format',
            os.environ.get(
                'GB_SHA_FORMAT',
                '{an}-{v}-sha256-{os}-{m}.json'
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

        self.sha = kwargs.get(
            'sha',
            Arguments.OPTION_SHA_INFO
        )

        self.work_dir = kwargs.get(
            'work_dir',
            os.environ.get(
                'GB_WORK_DIR',
                os.path.join(gravitybee.FILE_DIR, 'build', uuid.uuid1().hex[:16])
            )
        )

        if os.path.exists(self.work_dir):
            print(
                gravitybee.VERB_MESSAGE_PREFIX,
                "ERROR: work_dir must not exist. It may be deleted."
            )
            raise FileExistsError

        self.staging_dir = kwargs.get(
            'staging_dir',
            os.environ.get(
                'GB_STAGING_DIR',
                os.path.join(gravitybee.FILE_DIR, 'dist')
            )
        )

        self.with_latest = kwargs.get(
            'with_latest',
            False
        )

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

        pl_sys = platform.system().lower()
        self.operating_system = pl_sys if pl_sys != 'darwin' else 'osx'

        self.machine_type = platform.machine().lower()

        gravitybee.verboseprint("Arguments:")
        gravitybee.verboseprint("app_name:",self.app_name)
        gravitybee.verboseprint("app_version:",self.app_version)
        gravitybee.verboseprint("operating_system:",self.operating_system)
        gravitybee.verboseprint("machine_type:",self.machine_type)
        gravitybee.verboseprint("console_script:",self.console_script)
        gravitybee.verboseprint("pkg_name:",self.pkg_name)
        gravitybee.verboseprint("script_path:",self.script_path)
        gravitybee.verboseprint("pkg_dir:",self.pkg_dir)
        gravitybee.verboseprint("src_dir:",self.src_dir)
        gravitybee.verboseprint("name_format:",self.name_format)
        gravitybee.verboseprint("clean:",self.clean)
        gravitybee.verboseprint("work_dir:",self.work_dir)
        gravitybee.verboseprint("staging_dir:",self.staging_dir)
        gravitybee.verboseprint("with_latest:",self.with_latest)
        gravitybee.verboseprint("sha:",self.sha)

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
        gen_file: A str with name of file of the standalone
            application created.
        gen_file_w_path: A str with absolute path and name of file of
            the standalone application created.
    """

    ENVIRON_PREFIX = 'GB_ENV_'
    INFO_FILE = os.path.join(gravitybee.FILE_DIR, 'gravitybee-info.json')
    FILES_FILE = os.path.join(gravitybee.FILE_DIR, 'gravitybee-files.json')
    ENVIRON_SCRIPT = os.path.join(gravitybee.FILE_DIR, 'gravitybee-environs')
    ENVIRON_SCRIPT_POSIX_EXT = '.sh'
    ENVIRON_SCRIPT_WIN_EXT = '.bat'
    ENVIRON_SCRIPT_POSIX_ENCODE = 'utf-8'
    ENVIRON_SCRIPT_WIN_ENCODE = 'cp1252'
    EXTRA_PACKAGES_WINDOWS = ['packaging']
    EXTRA_MODULES_WINDOWS = ['packaging', 'packaging.version', 'packaging.specifiers']

    @classmethod
    def get_hash(cls, filename):
        """
        Finds a SHA256 for the given file.

        Args:
            filename: A str representing a file.
        """

        if os.path.exists(filename):
            sha256 = hashlib.sha256()
            with open(filename, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)
            return sha256.hexdigest()
        else:
            return None


    def __init__(self, args=None):

        self.args = args

        self.gen_file = None            # not set until file is created
        self.gen_file_w_path = None     # not set until file is created
        self.sha_file = None            # not set until file is created
        self.sha_file_w_path = None     # not set until file is created

        self.standalone_name = self.args.name_format.format(
            an=self.args.app_name,
            v=self.args.app_version,
            os=self.args.operating_system,
            m=self.args.machine_type
        )

        self.gb_dir, self.gb_filename = os.path.split(__file__)

        if not os.path.exists(self.args.work_dir):
            os.makedirs(self.args.work_dir)

        if not os.path.exists(gravitybee.FILE_DIR):
            os.makedirs(gravitybee.FILE_DIR)

        self._temp_script = os.path.join(
            self.args.work_dir,
            uuid.uuid1().hex[:16] + '_' + self.args.console_script + '.py'
        )

        gravitybee.verboseprint("Package generator:")
        gravitybee.verboseprint("standalone_name:",self.standalone_name)


    def _create_hook(self):
        # get the hook ready
        template = Template(
            open(
                os.path.join(
                    self.gb_dir,
                    "hook-template"
                ),
                "r"
            ).read()
        )

        hook = template.safe_substitute({ 'app_name': self.args.app_name })

        # 1 - extra data
        hook += "# collection extra data, if any (using --extra-data option)"
        try:
            for data in self.args.extra_data:
                hook += "\ndatas.append(('"
                hook += self.args.pkg_dir + os.sep
                if self.args.src_dir != '.':
                    hook += self.args.src_dir + os.sep
                hook += self.args.pkg_name + os.sep + data
                hook += "', '" + self.args.pkg_name + "/" + data + "'))"
                hook += "\n\n"
        except:
            pass

        # 2 - package metadata
        hook += "# add dependency metadata"
        for package in gravitybee.pyppy.get_required():
            #datas += copy_metadata(pkg)
            hook += "\ndatas += copy_metadata('" + package + "')"


        if self.args.operating_system == 'windows':
            for extra_package in self.EXTRA_PACKAGES_WINDOWS:
                if extra_package not in gravitybee.pyppy.get_required():
                    hook += "\ndatas += copy_metadata('" + extra_package + "')"

        hook += "\n"

        # 3 - write file
        self.hook_file = os.path.join(
            self.args.work_dir,
            "hook-" + self.args.pkg_name + ".py"
        )
        f = open(self.hook_file, "w+")
        f.write(hook)
        f.close()

        gravitybee.verboseprint("Created hook file:",self.hook_file)


    def _process_sha(self):

        gravitybee.verboseprint("Processing SHA256 hash info...")

        self.file_sha = PackageGenerator.get_hash(self.gen_file_w_path)

        if self.args.sha == Arguments.OPTION_SHA_FILE:

            # in memory version of file contents
            sha_dict = {}
            sha_dict[self.gen_file] = self.file_sha

            # file name
            self.sha_file = self.args.sha_format.format(
                an=self.args.app_name,
                v=self.args.app_version,
                os=self.args.operating_system,
                m=self.args.machine_type
            )

            gravitybee.verboseprint("SHA256 hash file:", self.sha_file)

            sha_file = open(self.sha_file, 'w')
            sha_file.write(json.dumps(sha_dict))
            sha_file.close()


    def _stage_artifacts(self):

        gravitybee.verboseprint("Staging artifacts...")

        # create directories
        if os.path.exists(self.args.staging_dir):
            gravitybee.verboseprint("Removing staging directory:", self.args.staging_dir)
            shutil.rmtree(self.args.staging_dir)

        os.makedirs(self.args.staging_dir)

        # version-based dir
        version_dst = os.path.join(
            self.args.staging_dir,
            self.args.app_version
        )
        if not os.path.exists(version_dst):
            os.makedirs(version_dst)

        shutil.move(self.gen_file_w_path, version_dst)

        # update path
        self.gen_file_w_path = os.path.join(
            version_dst,
            self.gen_file
        )

        gravitybee.verboseprint("Main artifact:", self.gen_file_w_path)

        # dir just called 'latest'
        if self.args.with_latest:

            gravitybee.verboseprint("Creating latest dir...")

            latest_dst = os.path.join(
                self.args.staging_dir,
                'latest'
            )
            if not os.path.exists(latest_dst):
                os.makedirs(latest_dst)

            gravitybee.verboseprint("Copying to latest...")

            shutil.copy2(self.gen_file_w_path, latest_dst)

            latest_standalone_name = self.args.name_format.format(
                an=self.args.app_name,
                v='latest',
                os=self.args.operating_system,
                m=self.args.machine_type
            )

            if self.gen_file.endswith(".exe"):
                latest_standalone_name += ".exe"

            os.rename(
                os.path.join(latest_dst, self.gen_file),
                os.path.join(latest_dst, latest_standalone_name)
            )

            gravitybee.verboseprint(
                "Latest artifact:",
                os.path.join(latest_dst, latest_standalone_name)
            )

        if self.args.sha == Arguments.OPTION_SHA_FILE:

            gravitybee.verboseprint("Staging SHA hash artifact:", self.sha_file)

            shutil.move(self.sha_file, version_dst)

            self.sha_file_w_path = os.path.join(
                version_dst,
                self.sha_file
            )

            gravitybee.verboseprint("SHA artifact:", self.sha_file_w_path)

            if self.args.with_latest:

                shutil.copy2(self.sha_file_w_path, latest_dst)

                latest_sha_file = self.args.sha_format.format(
                    an=self.args.app_name,
                    v='latest',
                    os=self.args.operating_system,
                    m=self.args.machine_type
                )

                os.rename(
                    os.path.join(latest_dst, self.sha_file),
                    os.path.join(latest_dst, latest_sha_file)
                )

                gravitybee.verboseprint(
                    "Latest SHA artifact:",
                    os.path.join(latest_dst, latest_sha_file)
                )


    def _write_info_files(self):

        if not self.args.dont_write_file:

            # GATHER INFO -------------------------------------------
            gb_info = {}
            gb_info['app_name'] = self.args.app_name
            gb_info['app_version'] = self.args.app_version
            gb_info['operating_system'] = self.args.operating_system
            gb_info['machine_type'] = self.args.machine_type
            gb_info['console_script'] = self.args.console_script
            gb_info['script_path'] = self.args.script_path
            gb_info['pkg_dir'] = self.args.pkg_dir
            gb_info['src_dir'] = self.args.src_dir
            gb_info['name_format'] = self.args.name_format
            gb_info['clean'] = self.args.clean
            gb_info['work_dir'] = self.args.work_dir
            gb_info['staging_dir'] = self.args.staging_dir
            gb_info['with_latest'] = self.args.with_latest
            gb_info['gen_file'] = self.gen_file
            gb_info['gen_file_w_path'] = self.gen_file_w_path
            gb_info['file_sha'] = self.file_sha

            if self.args.sha == Arguments.OPTION_SHA_FILE:
                gb_info['sha_file'] = self.sha_file
                gb_info['sha_file_w_path'] = self.sha_file_w_path
                gb_info['sha_format'] = self.args.sha_format

            gb_info['extra_data'] = []

            if self.args.extra_data is not None:
                for extra_data in self.args.extra_data:
                    gb_info['extra_data'].append(extra_data)

            # INFO file ---------------------------------------------
            gravitybee.verboseprint(
                "Writing information file:",
                PackageGenerator.INFO_FILE
            )
            info_file = open(PackageGenerator.INFO_FILE,'w')
            info_file.write(json.dumps(gb_info))
            info_file.close()

            # FILES file --------------------------------------------

            # create memory structure
            gb_files = []
            gb_file = {}
            gb_file['filename'] = self.gen_file
            gb_file['path'] = self.gen_file_w_path
            if self.gen_file.endswith(".exe"):
                gb_file['mime-type'] = 'application/vnd.microsoft.portable-executable'
            else:
                gb_file['mime-type'] = 'application/x-executable'
            gb_file['label'] = \
                self.args.app_name \
                + " Standalone Executable (" \
                + self.gen_file \
                + ") [GravityBee Build]"
            gb_files.append(gb_file)

            if self.args.sha == Arguments.OPTION_SHA_FILE:

                sha_file_info = {}
                sha_file_info['filename'] = self.sha_file
                sha_file_info['path'] = self.sha_file_w_path
                sha_file_info['mime-type'] = 'application/json'
                sha_file_info['label'] = \
                    "SHA256 Hash for " \
                    + self.gen_file
                gb_files.append(sha_file_info)

            # write to disk
            gravitybee.verboseprint(
                "Writing files file:",
                PackageGenerator.FILES_FILE
            )
            file_file = open(PackageGenerator.FILES_FILE, 'w')
            file_file.write(json.dumps(gb_files))
            file_file.close()

            # ENVIRONS ----------------------------------------------

            # remove attributes that aren't useful as exported
            # environs
            del gb_info['extra_data']
            del gb_info['name_format']
            del gb_info['sha_format']
            del gb_info['clean']

            gravitybee.verboseprint(
                "Writing environ script:",
                PackageGenerator.ENVIRON_SCRIPT \
                    + PackageGenerator.ENVIRON_SCRIPT_POSIX_EXT
            )
            shell = open(
                PackageGenerator.ENVIRON_SCRIPT \
                    + PackageGenerator.ENVIRON_SCRIPT_POSIX_EXT,
                mode = 'w',
                encoding = PackageGenerator.ENVIRON_SCRIPT_POSIX_ENCODE
            )

            for k, v in gb_info.items():
                shell.write("export ")
                shell.write(PackageGenerator.ENVIRON_PREFIX + k.upper())
                shell.write('="')
                shell.write(str(v))
                shell.write('"\n')

            shell.close()

            gravitybee.verboseprint(
                "Writing environ script:",
                PackageGenerator.ENVIRON_SCRIPT \
                    + PackageGenerator.ENVIRON_SCRIPT_WIN_EXT
            )

            bat = open(
                PackageGenerator.ENVIRON_SCRIPT \
                    + PackageGenerator.ENVIRON_SCRIPT_WIN_EXT,
                mode = 'w',
                encoding = PackageGenerator.ENVIRON_SCRIPT_WIN_ENCODE
            )

            for k, v in gb_info.items():
                bat.write("set ")
                bat.write(PackageGenerator.ENVIRON_PREFIX + k.upper())
                bat.write("=")
                bat.write(str(v))
                bat.write("\r\n")

            bat.close()


    def _cleanup(self):

        if self.args.clean:
            gravitybee.verboseprint("Cleaning up...")

            # clean work dir

            if os.path.isdir(self.args.work_dir):
                gravitybee.verboseprint("Deleting working dir:", self.args.work_dir)
                shutil.rmtree(self.args.work_dir)


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
            commands += [ '--hidden-import', pkg ]

        if self.args.operating_system == 'windows':
            for extra_package in self.EXTRA_PACKAGES_WINDOWS:
                if extra_package not in gravitybee.pyppy.get_required():
                    pyppyn.ConfigRep.install_package(extra_package)

        if self.args.operating_system == 'windows':
            for extra_module in self.EXTRA_MODULES_WINDOWS:
                pyppyn.ConfigRep.import_module(extra_module)
                commands += [ '--hidden-import', extra_module ]

        commands += [
            self._temp_script
        ]

        if self.args.operating_system != 'windows':
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

        # todo: add logging
        # todo: add stdout, stderr to logging
        # when not verbose, stdout is available here: result.stdout
        # when not verbose, stderr is available here: result.stderr

        # get info about standalone binary
        for standalone in glob.glob(
            os.path.join(
                self.args.work_dir,
                'dist',
                self.standalone_name + '*'
            )
        ):
            self.gen_file_w_path = standalone
            self.gen_file = os.path.basename(self.gen_file_w_path)
            gravitybee.verboseprint("Generated standalone file:", self.gen_file)

        self._process_sha()         # creates the sha files need for staging
        self._stage_artifacts()     # creates the file names needed to write
        self._write_info_files()    # write info (with paths from staging) and sha
        self._cleanup()
        return gravitybee.EXIT_OKAY

