dir-sync
========

(c) 2014 Thomas Khyn

Advanced directory tree synchronisation tool

based on `Python robocopier`_ by Anand B Pillai

`Python robocopier` .. http://code.activestate.com/recipes/231501-python-robocopier-advanced-directory-synchronizati/


Usage
-----

python robocopy.py <sourcedir> <targetdir> [options]


Main Options:
-------------

-d --diff          Only report difference between sourcedir and targetdir
-s, --synchronize  Synchronize content between sourcedir and targetdir
-u, --update       Update existing content between sourcedir and targetdir


Additional Options:
-------------------

-p, --purge        Purge files when synchronizing (does not purge by default).
-f, --force        Force copying of files, by trying to change file permissions.
-n, --nodirection  Update files in source directory from target
                   directory (only updates target from source by default).
-c, --create       Create target directory if it does not exist (By default,
                   target directory should exist.)
-m, --modtime      Only compare file's modification times for an update (By default,
                   compares source file's creation time also).
