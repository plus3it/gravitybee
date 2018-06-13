CHANGE LOG
==========

0.1.16 - 2018.06.21
-------------------
* [BUG FIX] Compatibility issues with Windows resolved.

0.1.15 - 2018.06.06
-------------------
* [BUG FIX] Losing ``.exe`` extension with Windows executables in the
  latest staging area.

0.1.14 - 2018.06.04
-------------------
* [BUG FIX] ``--with-latest`` was not working as a CL flag.

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
* [BUG FIX] Fix exit code (was returning True).
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
* [BUG FIX] Path bug.

0.1.1 - 2018.04.26
------------------
* [BUG FIX] Many bug fixes.

0.1.0 - 2018.04.20
------------------
* Initial release!
