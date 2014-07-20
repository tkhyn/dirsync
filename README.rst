dir-sync
========

|copyright| 2014 Thomas Khyn
|copyright| 2003 Anand B Pillai

Advanced directory tree synchronisation tool

based on `Python robocopier`_ by Anand B Pillai


Usage
-----

From the command line::

   dirsync.py <sourcedir> <targetdir> [options]

From python::

   from dir_sync import sync
   sync(sourcedir, targetdir, **options)


Main Options:
-------------

Chosing one option among the following ones is mandatory

-d, --diff            Only report difference between sourcedir and targetdir
-s, --synchronize     Synchronize content between sourcedir and targetdir
-u, --update          Update existing content between sourcedir and targetdir


Additional Options:
-------------------

--purge, -p             Purge files when synchronizing (does not purge by
                        default)
--force, -f             Force copying of files, by trying to change file
                        permissions
--nodirection, -n       Create target directory if it does not exist (By
                        default, target directory should exist.)
--create, -c            Only compare file's modification times for an update
                        (By default, compares source file's creation time
                        also)
--modtime, -m           Update existing content between sourcedir and
                        targetdir
--ignore, -x patterns   Patterns to ignore
--only, -o patterns     Patterns to include (exclude every other)
--exclude, -e patterns  Patterns to exclude
--include, -i patterns  Patterns to include (with precedence over excludes)

.. |copyright| unicode:: 0xA9

.. _`Python robocopier`: http://code.activestate.com/recipes/231501-python-robocopier-advanced-directory-synchronizati/
