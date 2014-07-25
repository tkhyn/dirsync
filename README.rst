dirsync
=======

|copyright| 2014 Thomas Khyn
|copyright| 2003 Anand B Pillai

Advanced directory tree synchronisation tool

based on `Python robocopier`_ by Anand B Pillai


Usage
-----

From the command line::

   dirsync <sourcedir> <targetdir> [options]

From python::

   from dirsync import sync
   sync(sourcedir, targetdir, **options)


Main Options:
-------------

Chosing one option among the following ones is mandatory

--diff, -d              Only report difference between sourcedir and targetdir
--sync, -s              Synchronize content between sourcedir and targetdir
--update, -u            Update existing content between sourcedir and targetdir


Additional Options:
-------------------

--verbose, -v           Provide verbose output
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
--ignore, -x patterns   Regex patterns to ignore
--only, -o patterns     Regex patterns to include (exclude every other)
--exclude, -e patterns  Regex patterns to exclude
--include, -i patterns  Regex patterns to include (with precedence over
                        excludes)

.. |copyright| unicode:: 0xA9

.. _`Python robocopier`: http://code.activestate.com/recipes/231501-python-robocopier-advanced-directory-synchronizati/
