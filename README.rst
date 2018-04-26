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

GravityBee helps you generate standalone Python applications.

GravityBee is targeted at python
programs that are already packaged in the standard setuptools
way.

These are some benefits of a GravityBee standalone application:

* You end up with one file that contains everything.
* Your user does not need to install Python or any packages.
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
    $ ls *cfg
    setup.cfg
    $ pip install --editable .
    $ pip install gravitybee

Step 2 - Provide (or gather) information
----------------------------------------

GravityBee will assume all necessary information when run. However, you may wish to override the assumed
values. You can provide values either through environment variables or command line flags. If both are
provided, command line flags take precedence.

Options [ENVIRONMENT VARIABLES]:

--app-name TEXT  [GB_APP_NAME] The name that will appear as part of the final standalone application name.
                    *Default:* ``name`` *from setup.py and/or setup.cfg.*

--pkg-name TEXT  [GB_PKG_NAME] The package name for the application you are building.
                    *Default: First value in* ``packages`` *from setup.py and/or setup.cfg, or if not
                    found, the value from --app-name.*

--script TEXT  [GB_SCRIPT] The path to the application file installed by ``pip`` when you installed
                    your application. Depending on your configuration, this may be determined by
                    ``options.entry_points.console_scripts`` from ``setup.py`` and/or ``setup.cfg``.
                    *Default:* ``$VIRTUAL_ENV/bin/app_name``

--src-dir TEXT  [GB_SRC_DIR] The relative path of the package containing your application.
                    *Default: None* 

--pkg-dir TEXT  [GB_PKG_DIR] The relative or absolute path of the package containing your application.
                    This directory must contain a ``setup.py`` file.
                    *Default:* ``.``

--extra-data TEXT  [GB_EXTRA_DATA] Relative to package directory, any extra directories or files that need
                    to be included, that wouldn't normally be included as Python code. Can be used multiple
                    times.
                    *Default: None*

If you are using environment variables, you could set them up like this.

.. code-block:: bash

    $ export GB_APP_NAME=coolapp
    $ export GB_PKG_NAME=coolapp
    $ export GB_SCRIPT=/usr/var/python/etc/coolapp


Step 3 - Generate
-----------------

Creating the standalone application is easy now.

.. code-block:: bash

    $ gravitybee --generate

If you are not using environment variables, you can combine steps 2 and 3.

.. code-block:: bash

    $ gravitybee --generate --app-name coolapp --script /usr/var/python/etc/coolapp --pkg-dir coolapp


Attribution
===========

The idea for GravityBee's core functionality comes from `Nicholas Chammas <https://github.com/nchammas>`
and his project `flintrock <https://github.com/nchammas/flintrock>`. Huge thanks to Nicholas!


Contribute
==========

GravityBee is hosted on `GitHub <http://github.com/YakDriver/gravitybee>`_ and is an open source project that welcomes contributions of all kinds from the community.

For more information about contributing, see `the contributor guidelines <https://github.com/YakDriver/gravitybee/CONTRIBUTING.rst>`_.


