CHANGE LOG
==========

0.1.29 - 2020.01.15
-------------------
* [ENHANCEMENT] Remove pipenv files and update setup.cfg dependency versions.

0.1.28 - 2020.01.14
-------------------
* [ENHANCEMENT] Bump version to include updated dependencies.

0.1.27 - 2019.05.06
-------------------
* [ENHANCEMENT] Bump version to include updated dependencies.

0.1.26 - 2019.02.05
-------------------
* [ENHANCEMENT] Fix distutils issue, improve error handling, update versions.

0.1.25 - 2019.01.31
-------------------
* [ENHANCEMENT] Add distutils to builds.

0.1.24 - 2019.01.29
-------------------
* [ENHANCEMENT] Clean up code, add community docs.
* [ENHANCEMENT] Transfer to Plus3IT.

0.1.23 - 2019.01.24
-------------------
* [FIX] Properly pin Pip so all dependencies are installed with pinned
  Pip version.
* [ENHANCEMENT] Restructure Travis CI linting, testing, deploying so
  deploy only happens when other stages complete successfully.
* [ENHANCEMENT] Improve speed of MacOS builds significantly.

0.1.22 - 2019.01.22
-------------------
* [ENHANCEMENT] Pin Pip and Pytest versions, adding ``requirements.txt``.

0.1.21 - 2019.01.10
-------------------
* [ENHANCEMENT] Lint code to conform with pylint and flake8 and add them
  Travis-CI tests.
* [ENHANCEMENT] Use ``pipenv`` and a lock file for dependency management.
* [ENHANCEMENT] Adjust for compatibility with Python 3.7.

0.1.20 - 2018.08.08
-------------------
* [ENHANCEMENT] Add ``--label-format`` option so that users can customize
  the label displayed for their applications in `gravitybee-files.json`.

0.1.19 - 2018.07.11
-------------------
* [ENHANCEMENT] Add ``--extra-pkgs`` and ``--extra-modules`` options for
  including additional packages and modules with standalone executables.

0.1.18 - 2018.07.05
-------------------
* [ENHANCEMENT] Add ``--onedir`` flag for improved debugging.

0.1.17 - 2018.06.27
-------------------
* [FIX] Compatibility issues with CentOS 6 resolved.

0.1.16 - 2018.06.21
-------------------
* [FIX] Compatibility issues with Windows resolved.

0.1.15 - 2018.06.06
-------------------
* [FIX] Losing ``.exe`` extension with Windows executables in the
  latest staging area.

0.1.14 - 2018.06.04
-------------------
* [FIX] ``--with-latest`` was not working as a CL flag.

0.1.13 - 2018.06.04
-------------------
* [ENHANCEMENT] Rearrange files created by GravityBee to all be
  contained in a ``.gravitybee`` subdirectory of the current
  directory.
* [ENHANCEMENT] Place the distribution artifacts in the staging
  directory, with a default value of ``.gravitybee/dist``.
* [ENHANCEMENT] Add option ``--staging-dir`` to specify directory
  where artifact staging should take place and export another
  environment variable ``GB_ENV_STAGING_DIR``.
* [ENHANCEMENT] Add option ``--with-latest`` to allow creation of
  a second artifact staging directory called "latest" containing
  the artifacts renamed with "latest" in the place of the version.
* [ENHANCEMENT] Add option ``--sha-format`` to allow custom naming
  of the SHA hash file.

0.1.12 - 2018.05.29
-------------------
* [ENHANCEMENT] Add OS and machine type to the SHA256 hash file (to
  avoid overwriting files if files from different platforms go to the
  same location).
* [ENHANCEMENT] Cleanup code with better variable names.

0.1.11 - 2018.05.24
-------------------
* [ENHANCEMENT] Create a SHA256 hash for the generated standalone
  file and include hash with file information and optionally in
  a separate file (using --sha flag).
* [ENHANCEMENT] Change names of environment variables produced
  with output scripts to be prefixed with GB_ENV so that the
  environs do not collide with environs consumed by GravityBee.
* [ENHANCEMENT] Provide a convenience cleanup Bash script to
  remove GravityBee output files (e.g., json and generated
  executables).
* [ENHANCEMENT] Cleanup code with more constants.

0.1.10 - 2018.05.21
-------------------
* [ENHANCEMENT] Provide two additional output files for importing
  GravityBee information into the environment on POSIX and Windows
  platforms.

0.1.9 - 2018.05.14
------------------
* [ENHANCEMENT] Output file with run info in json format for easy
  consumption by other tools.

0.1.8 - 2018.05.11
------------------
* [ENHANCEMENT] In non-verbose mode, allow for supressing stdout and
  stderr from pyinstaller, which can be sizeable.
* [ENHANCEMENT] Change name of ``gravitybee.file`` to
  ``gravitybee-files.json``.

0.1.7 - 2018.05.11
------------------
* [FIX] Fix exit code (was returning True).
* [ENHANCEMENT] Automatically find console script installed by
  setuptools on Windows and Linux and variety of places.

0.1.6 - 2018.05.03
------------------
* [ENHANCEMENT] Follow format prescribed by satsuki for output
  file (potential for multiple files).

0.1.5 - 2018.05.01
------------------
* [ENHANCEMENT] Add mime-type and label to .json formatted file
  information stored in gravitybee.file.

0.1.3 - 2018.05.01
------------------
* [ENHANCEMENT] Create gravitybee.file with name of standalone
  application.

0.1.2 - 2018.04.27
------------------
* [ENHANCEMENT] Provide standalone file and path.
* [FIX] Path bug.

0.1.1 - 2018.04.26
------------------
* [FIX] Many bug fixes.

0.1.0 - 2018.04.20
------------------
* Initial release!
