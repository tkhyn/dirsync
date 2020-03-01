dirsync
=======

|copyright| 2014-2019 Thomas Khyn
|copyright| 2003-2015 Anand B Pillai

Advanced directory tree synchronisation tool

based on `Python robocopier`_ by Anand B Pillai

If you like dirsync and are looking for a way to thank me and/or encourage
future development, here is my BTC or BCH donation address:
``1EwENyR8RV6tMc1hsLTkPURtn5wJgaBfG9``.

Usage
-----

From the command line::

   dirsync <sourcedir> <targetdir> [options]

From python::

   from dirsync import sync
   sync(sourcedir, targetdir, action, **options)

For instance, if you synchronize dirA with dirB located in the current working directory, do as follows::

   sync('./dirA', './dirB', action="sync", purge=True)


Main Options
------------

Chosing one option among the following ones is mandatory

--diff, -d              Only report difference between sourcedir and targetdir
--sync, -s              Synchronize content between sourcedir and targetdir
--update, -u            Update existing content between sourcedir and targetdir

If you use one of the above options (e.g. ``sync``) most of the time, you
may consider defining the ``action`` option in a `Configuration file`_ parsed
by dirsync.


Additional Options
------------------

--verbose, -v           Provide verbose output
--purge, -p             Purge files when synchronizing (does not purge by
                        default)
--force, -f             Force copying of files, by trying to change file
                        permissions
--twoway, -2            Update files in source directory from target
                        directory (only updates target from source by default)
--create, -c            Create target directory if it does not exist (By
                        default, target directory should exist.)
--ctime                 Also takes into account the source file\'s creation
                        time (Windows) or the source file\'s last metadata
                        change (Unix)
--content               Takes into account ONLY content of files. 
                        Synchronize ONLY different files.
                        At two-way synchronization source files content 
                        have priority if destination and source are existed
--ignore, -x patterns   Regex patterns to ignore
--only, -o patterns     Regex patterns to include (exclude every other)
--exclude, -e patterns  Regex patterns to exclude
--include, -i patterns  Regex patterns to include (with precedence over
                        excludes)


Configuration file
------------------

.. note::
   Configuration files are only used when using the command line, and ignored
   when dirsync is called from within Python.

If you want to use predefined options all the time, or if you need specific
options when 'dirsyncing' a specific source directory, dirsync looks for
two configuration files, by order or priority (the last takes precedence)::

    ~/.dirsync
    source/directory/.dirsync

.. note::
   A ~/.dirsync configuration file is automatically created the first time
   dirsync is ran from the command line. It enables ``sync`` mode by default.

.. warning::
   Any ``source/directory/.dirsync`` file is automatically excluded from the
   files to compare. You have to explicitly include using the ``--include``
   option it if you want it to be covered by the comparison.

The command line options always override the values defined in the
configuration files.

The configuration files must have a ``defaults`` section, and the options are
as defined above. The only exception is for the option ``action``, which can
take 3 values ``diff``, ``sync`` or ``update``.

Example config file::

   [defaults]
   action = sync
   create = True


Custom logger
-------------

From python, you may not want to have the output sent to ``stdout``. To do so,
you can simply pass your custom logger via the ``logger`` keyword argument of
the ``sync`` function::

   sync(sourcedir, targetdir, action, logger=my_logger, **options)


.. |copyright| unicode:: 0xA9

.. _`Python robocopier`: http://code.activestate.com/recipes/231501-python-robocopier-advanced-directory-synchronizati/
