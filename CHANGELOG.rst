CHANGE LOG
==========

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
