"""
dirsync's functions
"""

from __future__ import print_function

import sys
import os

from .syncer import Syncer


def sync(sourcedir, targetdir, action, **options):

    copier = Syncer(sourcedir, targetdir, action, **options)
    copier.do_work()

    # print report at the end
    copier.report()

    return set(copier._changed).union(copier._added).union(copier._deleted)


def from_cmdline():
    from .options import ArgParser, USER_CFG_FILE, DEFAULT_USER_CFG

    # create config file if it does not exist
    user_cfg_file = os.path.expanduser(USER_CFG_FILE)
    if not os.path.isfile(user_cfg_file):
        print('Creating user config file "%s" ...' % user_cfg_file, end=''),
        f = open(user_cfg_file, 'w').write(DEFAULT_USER_CFG)
        f.close()
        print(' Done')

    try:
        sync(**vars(ArgParser().parse_args()))
    except Exception as e:
        sys.stdout.write(str(e) + '\n')
        sys.exit(2)
