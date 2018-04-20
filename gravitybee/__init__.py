# -*- coding: utf-8 -*-
"""gravitybee module.

This module helps give programmatic access to the setup configuration
of a package and allows automatic installation of required packages
and importing of modules. This can be useful for automated
environments.

This module can be used by python scripts or through the included command-
line interface (CLI).

gravitybee, like the hobbit, is small but mighty. This module is named in
honor of Pippin, a companion, friend, Bichon Frise-Shih Tzu mix. He
passed away on March 30, 2018 at the age of 12 after a battle with
diabetes, blindness, deafness, and loss of smell. Pleasant to the
end, he was a great, great dog.
PIPPIN: I didn't think it would end this way.
GANDALF: End? No, the journey doesn't end here. Death is just another
    path, one that we all must take.

Example:
    Help using the gravitybee CLI can be found by typing the following::

        $ gravitybee --help

Todo:
    * Improve support for setup.py (support now focuses on setup.cfg)
"""
import platform
import sys
import pkg_resources
import os
import importlib

from distlib import database
from setuptools import config
from distutils import errors

__version__ = "0.2.3"

class ConfigRep(object):
    """Utility for reading setup.cfg and installing dependencies.

    This class helps find packages that must be installed as
    dependencies of a given package, based on a configuration file.
    In automated environments or when using automation to create
    standalone applications, it can be helpful to have programmatic
    access to this information.

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

    @classmethod
    def package_to_module(cls, package):
        """Attempts to find the module associated with a package.

        For example, given the PyYAML package, it will return yaml.
        For packages with multiple modules (e.g., pywin32) and
        submodules, this will only give the first module it finds.

        Args:
            package: A str of the package for which you want the
                associated module.

        Returns:
            A str of the module associated with the given package.

        Todo:
            * Add support for packages with multiple modules.
            * This needs more cross-platform testing.
        """
        dp = database.DistributionPath(include_egg=True)
        dist = dp.get_distribution(package)

        if dist is None:
            raise ImportError

        module = package # until we figure out something better

        for filename, _, _ in dist.list_installed_files():
            if filename.endswith(('.py')):

                parts = os.path.splitext(filename)[0].split(os.sep)

                if len(parts) == 1: # windows sep varies with distribution type
                    parts = os.path.splitext(filename)[0].split('/')

                if parts[-1].startswith('_') and not parts[-1].startswith('__'):
                    continue # ignore internals
                elif filename.endswith('.py') and parts[-1] == '__init__':
                    module = parts[-2]
                    break

        return module

    @classmethod
    def install_and_import(cls, package):
        """Installs a package and imports the associated module.

        Args:
            package: A str of the package to install.

        Returns:
            A str of the module that was imported after the package
            was installed.
        """
        try:
            module = cls.package_to_module(package)
            importlib.import_module(module)

        except (ImportError):
            import pip
            pip.main(['install', package])
            module = cls.package_to_module(package)

        finally:
            globals()[module] = importlib.import_module(module)

        return module

    _message_prefix = "[gravitybee]"
    _should_load = 0
    _did_load = 0
    _state = "INIT" # Valid values are INIT, READ, LOAD, and INSTALLED

    def __init__(self, *args, **kwargs):
        """Instantiation"""

        # Initial values
        self.setup_file = kwargs.get('setup_file',"setup.cfg")
        self.platform = kwargs.get('platform',platform.system()).lower()
        self.verbose = kwargs.get('verbose',False)

        # Verbose function
        self.verboseprint = lambda *a: print(ConfigRep._message_prefix, *a) if self.verbose else lambda *a, **k: None

        # Verbose output
        self.verboseprint("Verbose mode")
        self.verboseprint("Platform:",self.platform)
        self.verboseprint("Setup file:",self.setup_file)

    def process_config(self):
        """Convenience method to perform all steps with one call."""
        return self.read_config() and \
            self.load_config() and \
            self.install_packages()

    def read_config(self):
        """Reads the config file given through constructor."""
        self.verboseprint("Reading config file:",self.setup_file)
        self.config_dict = config.read_configuration(self.setup_file)
        self._state = "READ"
        return self.config_dict is not None

    def load_config(self):
        # Check that config has been read
        if self._state != "READ":
            self.read_config()

        """Loads the config file into data structures."""
        self.python_version = sys.version_info[0] + (sys.version_info[1]/10)
        self.app_version = str(self.config_dict["metadata"]["version"]).lower()

        self.verboseprint("This Python:",self.python_version)
        self.verboseprint("Version from",self.setup_file,":",self.app_version)

        """ Parsing some (but not all) possible markers.
        Compound markers (e.g., 'platform_system == "Windows" and python_version < "2.7"') and
        conditional markers (e.g., "pywin32 >=1.0 ; sys_platform == 'win32'") are not
        supported yet. """
        self.this_os_reqs = []      # Requirements on this os/env
        self.other_reqs = []        # Not required on this os/env, mostly included for debug so you can see where everything went
        self.base_reqs = []         # Across the board reqs
        self.this_python_reqs = []  # This python version reqs

        for r in pkg_resources.parse_requirements(self.config_dict["options"]["install_requires"]):

            if str(getattr(r, 'marker', 'None')) != 'None':
                """ Plain markers have 3 parts, 1. key, 2. conditional, 3. value
                Compound markers (not supported) will produce 3 markers,
                1. platform_system == "Windows", 2. and, 3. python_version == "2.7"
                https://github.com/pypa/setuptools/blob/master/pkg_resources/_vendor/packaging/markers.py
                https://www.python.org/dev/peps/pep-0496/ """
                for m in r.marker._markers:
                    if str(m[0]) == 'platform_system' and str(m[1]) == '==' and str(m[2]).lower() == self.platform:
                        self.this_os_reqs.append(r.key)

                    elif str(m[0]) == 'platform_system' and str(m[1]) == '==' and str(m[2]).lower() != self.platform:
                        self.other_reqs.append(r.key)

                    elif str(m[0]) == 'python_version':
                        if str(m[1]) == '<' and self.python_version < float(str(m[2])):
                            self.this_python_reqs.append(r.key)
                        elif str(m[1]) == '>' and self.python_version > float(str(m[2])):
                            self.this_python_reqs.append(r.key)
                        elif str(m[1]) == '>=' and self.python_version >= float(str(m[2])):
                            self.this_python_reqs.append(r.key)
                        elif str(m[1]) == '<=' and self.python_version <= float(str(m[2])):
                            self.this_python_reqs.append(r.key)
                        elif str(m[1]) == '!=' and self.python_version != float(str(m[2])):
                            self.this_python_reqs.append(r.key)
                        elif str(m[1]) == '==' and self.python_version == float(str(m[2])):
                            self.this_python_reqs.append(r.key)
                        else:
                            self.other_reqs.append(r.key)

                    else:
                        self.base_reqs.append(r.key) # if can't figure out the marker, add it

            else:
                self.base_reqs.append(r.key)

        self.verboseprint("Install Requires:")
        self.verboseprint("\tGenerally required:", self.base_reqs)
        self.verboseprint("\tFor this OS:", self.this_os_reqs)
        self.verboseprint("\tFor this Python version:", self.this_python_reqs)
        self.verboseprint("\tOthers listed by not required (e.g., wrong platform):", self.other_reqs)

        self._should_load = len(self.base_reqs) + len(self.this_os_reqs) + len(self.this_python_reqs)

        self._state = "LOAD"

        return self._should_load > 0

    def install_packages(self):
        if self._state != "LOAD":
            self.load_config()

        """Installs all needed packages from the config file."""
        for package in self.this_os_reqs + self.this_python_reqs + self.base_reqs:
            self.verboseprint("Installing package:", package)
            module = ConfigRep.install_and_import(package)
            self.verboseprint("Imported module:", module)
            self._did_load += 1

        self._state = "INSTALLED"

        return self._did_load == self._should_load

    def get_required(self):
        if self._state != "LOAD" and self._state != "INSTALLED":
            self.load_config()

        return self.base_reqs + self.this_os_reqs + self.this_python_reqs
