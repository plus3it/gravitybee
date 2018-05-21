==========
GravityBee
==========

.. image:: https://img.shields.io/github/license/YakDriver/gravitybee.svg
    :target: ./LICENSE
    :alt: License
.. image:: https://travis-ci.org/YakDriver/gravitybee.svg?branch=master
    :target: http://travis-ci.org/YakDriver/gravitybee
    :alt: Build Status
.. image:: https://img.shields.io/pypi/pyversions/gravitybee.svg
    :target: https://pypi.python.org/pypi/gravitybee
    :alt: Python Version Compatibility
.. image:: https://img.shields.io/pypi/v/gravitybee.svg
    :target: https://pypi.python.org/pypi/gravitybee
    :alt: Version

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

GravityBee depends on `Pyppyn <https://github.com/YakDriver/pyppyn>`_ and
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
                                        This directory must contain a ``setup.py`` file.
                                        *Default:* ``.``
(None)            --verbose, -v         Verbose mode.
GB_EXTRA_DATA     --extra-data, -e      Relative to package directory, any extra
                                        directories or files that need
                                        to be included, that wouldn't normally be
                                        included as Python code. Can be used multiple
                                        times.
                                        *Default: None*
GB_WORK_DIR       --work-dir, -w        Directory for use by GravityBee to build
                                        application. Cannot be an existing
                                        directory as it will be deleted if the clean
                                        option is used.
                                        *Default:* ``gb_workdir_<uuid>``
(None)            --clean, -c           Whether to clean up the work directory after
                                        the build. If used, GravityBee will copy the
                                        built standalone application to the current
                                        directory before deleting.
                                        *Default: Not*
GB_NAME_FORMAT    --name-format, -f     Format to be used in naming the standalone
                                        application. Must include
                                        {an}, {v}, {os}, {m}
                                        for app name, version, os, and machine
                                        type respectively.
                                        *Default:* ``{an}-{v}-standalone-{os}-{m}``
(None)            --no-file             Do not write the output files (see below).
                                        *Default: Will write
                                        files*
================  ==================    ==========================================




If you are using environment variables, you could set them up like this.

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
  ``created_file``, ``created_path``, and ``extra_data``.
* **gravitybee-environs.sh**: A shell file that can be sourced on
  POSIX platforms
  to create environment variables with GravityBee information. Each
  is prefixed
  with ``GB_``.
* **gravitybee-environs.bat**: A batch file that can be used to
  create environment variables with GravityBee information on
  Windows. Each
  environ is prefixed with ``GB_``.


The Test Example
----------------

Here is the file/package structure of the included
`test application <https://github.com/YakDriver/gravitybee/tree/dev/tests/gbtestapp>`_.

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
    $ gravitybee --src-dir src --extra-data gbextradata --verbose --clean


From Python Example
-------------------

Using GravityBee from a Python script is also possible. Using the
sample test app, here's some example code.

.. code-block:: python

    import gravitybee

    args = gravitybee.Arguments(
        src_dir="src",
        extra_data=["gbextradata"],
        verbose=True,
        pkg_dir=os.path.join("tests", "gbtestapp"),
        clean=True
    )

    pg = gravitybee.PackageGenerator(args)
    pg.generate()

    # show path (and name) of standalone app
    print("The standalone app: ", pg.created_path)


Attribution
===========

The idea for GravityBee's core functionality comes from `Nicholas Chammas <https://github.com/nchammas>`_
and his project `flintrock <https://github.com/nchammas/flintrock>`_. Huge thanks to Nicholas!


Contribute
==========

GravityBee is hosted on `GitHub <http://github.com/YakDriver/gravitybee>`_ and is an open source project that welcomes contributions of all kinds from the community.

For more information about contributing, see `the contributor guidelines <https://github.com/YakDriver/gravitybee/CONTRIBUTING.rst>`_.


