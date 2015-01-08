"""
dirsync's functions
"""

import sys

from .syncer import Syncer


def sync(sourcedir, targetdir, action, **options):

    copier = Syncer(sourcedir, targetdir, action, **options)
    copier.do_work()

    # print report at the end
    copier.report()

    return set(copier._changed).union(copier._added).union(copier._deleted)


def from_cmdline():
    from .options import ArgParser

    try:
        sync(**vars(ArgParser().parse_args()))
    except Exception, e:
        sys.stdout.write(str(e) + '\n')
        sys.exit(2)
