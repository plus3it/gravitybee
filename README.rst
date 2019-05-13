==========
GravityBee
==========

.. image:: https://img.shields.io/github/license/plus3it/gravitybee.svg
    :target: ./LICENSE
    :alt: License
.. image:: https://travis-ci.org/plus3it/gravitybee.svg?branch=master
    :target: http://travis-ci.org/plus3it/gravitybee
    :alt: Build Status
.. image:: https://img.shields.io/pypi/pyversions/gravitybee.svg
    :target: https://pypi.python.org/pypi/gravitybee
    :alt: Python Version Compatibility
.. image:: https://img.shields.io/pypi/v/gravitybee.svg
    :target: https://pypi.python.org/pypi/gravitybee
    :alt: Version
.. image:: https://pullreminders.com/badge.svg
    :target: https://pullreminders.com?ref=badge
    :alt: Pull Reminder

GravityBee helps you generate standalone applications for Windows,
Mac, and Linux from your Python applications.

GravityBee is targeted at Python
programs that are already packaged in the standard setuptools
way.

These are some benefits of a GravityBee standalone application:

* You end up with one file that contains everything.
* Your users do not need Python or any packages installed.
* You build separate natively executable applications for each of
  your target platforms.

GravityBee depends on `Pyppyn <https://github.com/plus3it/pyppyn>`_ and
`PyInstaller <http://www.pyinstaller.org>`_ and is subject to their limitations.

To Build A Standalone Application
=================================

Step 1 - Install
----------------

You must install the application you wish to build (e.g.,
``yoursuperapp``), as well as GravityBee.

.. code-block:: bash

    $ pip install yoursuperapp gravitybee

The process will also work fine if you're installing from a local
version of your app.

.. code-block:: bash

    $ cd yoursuperapp
    $ ls setup*
    setup.cfg            setup.py
    $ pip install --editable .
    $ pip install gravitybee

Step 2 - Provide (or gather) information
----------------------------------------

GravityBee will assume all necessary information when run. However,
you may wish to override the assumed
values. You can provide values either through environment variables
or command line flags. If both are
provided, command line flags take precedence.

Local logging can be configured in ``gravitybee/logging.conf``.

Options:

================  ==================    ==========================================
ENV VAR           CL Options            Desciption
================  ==================    ==========================================
GB_APP_NAME       --app-name, -a        The name that will appear as part of the
                                        final standalone application name.
                                        *Default:* ``name`` *from setup.py and/or
                                        setup.cfg.*
GB_PKG_NAME       --pkg-name, -n        The package name for the application you are
                                        building.
                                        *Default: First value in* ``packages`` *from
                                        setup.py and/or setup.cfg,
                                        or if not found, the value from --app-name.*
GB_SCRIPT         --script, -s          The path to the application file installed by
                                        ``pip`` when you installed
                                        your application. Depending on your
                                        configuration, this may be determined by
                                        ``options.entry_points.console_scripts`` from
                                        ``setup.py`` and/or ``setup.cfg``.
                                        *Default:* ``$VIRTUAL_ENV/bin/app_name``
GB_SRC_DIR        --src-dir, -d         The relative path of the package containing
                                        your application.
                                        *Default:* ``.``
GB_PKG_DIR        --pkg-dir, -p         The relative or absolute path of the package
                                        containing your application.
                                        This directory must contain a
                                        ``setup.py`` file.
                                        *Default:* ``.``
GB_EXTRA_DATA     --extra-data, -e      Relative to package directory, any extra
                                        directories or files that need
                                        to be included, that wouldn't normally
                                        be included as Python code. Can be
                                        used multiple times.
                                        *Default: None*
GB_WORK_DIR       --work-dir, -w        Directory for use by GravityBee to build
                                        application. Cannot be an existing
                                        directory as it will be deleted if the
                                        clean
                                        option is used.
                                        *Default:* ``.gravitybee/build/<uuid>``
GB_ONEDIR         --onedir              Instead of packaging into one file,
                                        package in one directory. This option
                                        is not compatible with producing a SHA
                                        hash since a hash is produced on a
                                        single file. This option may be useful
                                        for debugging runtimes errors in built
                                        applications.
                                        *Default: Not*
GB_CLEAN          --clean, -c           Flag indicating whether to
                                        clean up the work directory
                                        after
                                        the build.
                                        *Default: Not*
GB_NAME_FORMAT    --name-format, -f     Format to be used in naming the standalone
                                        application. Can include
                                        {an}, {v}, {os}, {m}
                                        for app name, version, os, and machine
                                        type respectively. On Windows, ``.exe``
                                        will be added automatidally.
                                        *Default:* ``{an}-{v}-standalone-{os}-{m}``
GB_SHA_FORMAT     --sha-format          Format to be used in naming the SHA hash
                                        file. Can include
                                        {an}, {v}, {os}, {m}
                                        for app name, version, os, and machine
                                        type respectively.
                                        *Default:* ``{an}-{v}-sha256-{os}-{m}.json``
GB_LABEL_FORMAT   --label-format        Format to be used in labeling the standalone
                                        application in `gravitybee-files.json`.
                                        Can include {An},
                                        {an}, {v}, {os}, {m}, and {ft}
                                        for capitalized application
                                        name, lowercase app name, version, OS,
                                        machine, and file type ("Standalone
                                        Executable" or
                                        "Standalone Executable SHA256 Hash")
                                        respectively. On Windows, ``.exe``
                                        will be added automatically.
                                        *Default:* ``{An} {v} {ft} for {os} [GravityBee Build]``
GB_NO_FILE        --no-file             Flag indicating to not write
                                        the output files (see below).
                                        If the ``--sha`` option is used to
                                        write a
                                        hash to a file, that file will
                                        still be
                                        written regardless.
                                        *Default: Will write
                                        files*
GB_SHA            --sha                 Option of where to put SHA256
                                        hash for generated file.
                                        Valid options are ``file``
                                        (create a separate file with
                                        hash), or ``info`` (only
                                        include the hash in the file
                                        info output). *Default:* ``info``
GB_STAGING_DIR    --staging-dir         Option to indicate where GravityBee
                                        should stage build artifacts
                                        (standalone executable and hash
                                        file). Two subdirectories can
                                        be created, one based on version
                                        and the other called "latest."
                                        *Default:* ``.gravitybee/dist``
GB_WITH_LATEST    --with-latest         Flag to indicate if GravityBee
                                        should create a "latest"
                                        directory in the staging area
                                        with a copy of the artifacts.
                                        *Default: Not*
GB_EXTRA_MODULES  --extra-modules       Any extra modules to be included with
                                        the standalone executable.
                                        *Default: None*
GB_EXTRA_PKGS     --extra-pkgs          Any extra packages to be included with
                                        the standalone executable.
                                        *Default: None*
================  ==================    ==========================================




If you are using environment variables, you could set them up like
this.

.. code-block:: bash

    $ export GB_APP_NAME=coolapp
    $ export GB_PKG_NAME=coolapp
    $ export GB_SCRIPT=/usr/var/python/etc/coolapp


Step 3 - Generate
-----------------

Creating the standalone application is easy now.

.. code-block:: bash

    $ gravitybee

If you are not using environment variables, you can combine steps 2 and 3.

.. code-block:: bash

    $ gravitybee --app-name coolapp --script /usr/var/python/etc/coolapp --pkg-dir coolapp

Output Files
------------

If the ``--no-file`` flag is not used, GravityBee will create output
files. These include:

* **gravitybee-files.json**: A JSON file that contains information
  about the standalone application generated by GravityBee including
  ``filename``, ``path``, ``mime-type``, and ``label`` as a list of
  dicts.
* **gravitybee-info.json**: A JSON file that contains information
  extracted
  about the application including ``app_name``, ``app_version``,
  ``console_script``,
  ``script_path``, ``pkg_dir``, ``src_dir``, ``name_format``,
  ``clean``, ``work_dir``,
  ``gen_file``, ``gen_file_w_path``, and ``extra_data``.
* **gravitybee-environs.sh**: A shell file that can be sourced on
  POSIX platforms
  to create environment variables with GravityBee information. Each
  is prefixed
  with ``GB_ENV_``.
* **gravitybee-environs.bat**: A batch file that can be used to
  create environment variables with GravityBee information on
  Windows. Each
  environ is prefixed with ``GB_ENV_``.


The Test Example
----------------

Here is the file/package structure of the included
`test application <https://github.com/plus3it/gravitybee/tree/dev/tests/gbtestapp>`_.

.. code-block:: bash

    gbtestapp
    |-- setup.py
    |-- setup.cfg
    >-- src
    |   >-- gbtestapp
    |       |-- __init__.py
    |       |-- cli.py
    |       >-- gbextradata
    |           |-- __init__.py
    |           |-- data_file.txt

You would build the application as follows. Since the application
package is under the ``src`` directory, you need to let GravityBee
know. Also, since we need to include the ``data_file.txt`` file,
we'll use the ``--extradata`` option to include the containing
directory (``gbextradata``).

.. code-block:: bash

    $ cd gbtestapp
    $ gravitybee --src-dir src --extra-data gbextradata --clean


From Python Example
-------------------

Using GravityBee from a Python script is also possible. Using the
sample test app, here's some example code.

.. code-block:: python

    import gravitybee

    args = gravitybee.Arguments(
        src_dir="src",
        extra_data=["gbextradata"],
        pkg_dir=os.path.join("tests", "gbtestapp"),
        clean=True
    )

    pg = gravitybee.PackageGenerator(args)
    pg.generate()

    # show path (and name) of standalone app
    print("The standalone app: ", pg.gen_file_w_path)


Attribution
===========

The idea for GravityBee's core functionality comes from `Nicholas Chammas <https://github.com/nchammas>`_
and his project `flintrock <https://github.com/nchammas/flintrock>`_. Huge thanks to Nicholas!


Contribute
==========

GravityBee is hosted on `GitHub <http://github.com/plus3it/gravitybee>`_ and is an open source project that welcomes contributions of all kinds from the community.

For more information about contributing, see `the contributor guidelines <https://github.com/plus3it/gravitybee/CONTRIBUTING.rst>`_.


