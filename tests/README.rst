dirsync tests
=============

If you are reading this, you're interested in contributing to this software.
Great news!

Before you start playing around, you may need the information that follows,
especially if you're not familiar with zc.buildout and/or tox.


The tests
---------

dirsync uses nose_ for testing. All the tests are in the
``tests`` directory, and the nose test runner uses the ``all-modules`` option
which is defined in ``tests/setup.cfg``. This means that any object which is
not intended to contain tests (e.g. a base classes module) shall contain the
statement ``__test__ = False``.

The ``setup.cfg`` file also contains coverage pre-configuration information,
but coverage is disabled by default.

Using buildout
--------------

This software uses zc.buildout_ to generate tests scripts. In (very) short
if you have never heard of it, zc.buildout is a tool to assemble given
versions of libraries together in completely isolated virtual environments,
ensuring robustness and repeatability. Its most common usage is to generate
scripts or builds.

You don't even need to install it globally nor in a virtual environment as it
has its own local installation script. To locally install buildout, go to the
main directory (where the ``buildout.cfg`` and ``bootstrap.py`` lie),
and type::

   $ python bootstrap.py

This will create a ``buildout`` script in a ``bin`` folder. Now you just have
to run::

   $ bin/buildout

It may take a few minutes to download and install the dependencies in the
*local* folder, and generate the scripts as defined in the ``buildout.cfg``
file.

You'll end up with:

bin/python
   An interpreter with all the relevant librairies in ``sys.path``, so that
   you can experiment in the actual environment of the software, with the
   versions that are specified in the buildout configuration and that are
   used for the tests.

bin/tests
   This script runs the test suite. See below, `Running the tests`_.

bin/coverage
   This script runs the test suite and outputs coverage information.

.. tip::
   If you don't want the packages to be downloaded and installed each time
   you run ``buildout`` or each time you change a version in ``buildout.cfg``,
   you may want to consider using a ``~/.buildout/default.cfg`` file to specify
   download and eggs installation paths using the ``download-cache`` and
   ``eggs-directory`` options.


Running the tests
-----------------

Simply generate the ``bin/tests`` script and, from the root directory, type::

   $ bin/tests

For coverage information, you can add ``--with-coverage`` to the above test
command but it's more convenient to use the shortcut::

   $ bin/coverage

You may want to run the test suite manually from the command line (to launch
tests from within an IDE, for example). To do this:

   - make sure that all the required dependencies are satisfied in the
     environment you are working in
   - add the main directory (where ``setup.py`` lies) to ``PYTHONPATH``
   - set the working directory to ``tests``

And simply use::

   $ nosetests [further_options]


Running the tox suite
---------------------

This software also uses tox_ to test against various environments (mainly
python and django versions).

While buildout is great to test against given versions of libraries with a
given interpreter (the one you used to run ``python bootstrap.py``), tox
focuses on running commands in various environments (the ones the users of the
software will run it in). It basically creates virtual environments and runs
the test suite (possibly with adaptations) in each of these environments.

Running the tox suite is just a matter of installing tox and running it from
the main directory::

   $ pip install tox
   $ tox


.. _nose: http://nose.readthedocs.org/en/latest/
.. _django_nose: https://pypi.python.org/pypi/django-nose
.. _zc.buildout: http://www.buildout.org/en/latest/
.. _tox: https://testrun.org/tox/
