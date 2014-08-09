"""
dirsync's functions
"""

import os
import sys
try:
    from ConfigParser import ConfigParser  # python 2
except ImportError:
    from configparser import ConfigParser  # python 3

from six import string_types, iteritems

from .syncer import Syncer


def sync(src_dir, tgt_dir, action, **options):

    copier = Syncer(src_dir, tgt_dir, action=action, **options)
    copier.do_work()

    # print report at the end
    copier.report()

    return set(copier._changed).union(copier._added).union(copier._deleted)


def execute_from_command_line():
    import argparse
    from .options import OPTIONS

    parser = argparse.ArgumentParser(
        description='Syncer: Command line directory diff, synchronization, '
                    'update & copy\n'
                    'Authors: Anand Pillai (v1.0), Thomas Khyn (v2.x)')

    parser.add_argument('sourcedir',
                        action='store',
                        help='Source directory')
    parser.add_argument('targetdir',
                        action='store',
                        help='Target directory')

    for opt, args in iteritems(OPTIONS):
        parser.add_argument('--' + opt, *args[0], **args[1])

    # now load default options from configuration file:
    # - from a current working directory dirsync.cfg file
    # - and/or a %HOME%/.dirsync user config file

    cfg_files = [os.path.join(os.getcwd(), 'dirsync.cfg')]
    home_dir = os.environ.get('HOME', None)
    if home_dir:
        # inserting in first position so that it is overriden by cwd conf file
        cfg_files.insert(0, os.path.join(home_dir, '.dirsync'))

    cfg = ConfigParser()
    cfg.read(cfg_files)

    for name, val in cfg.items('defaults'):
        try:
            opt = OPTIONS[name][1]
        except KeyError:
            if opt == 'action' and val in OPTIONS:
                OPTIONS[val]['default'] = True
            continue

        curdef = opt.get('default', '')
        if isinstance(curdef, bool):
            newdef = val not in ('0', 'False', 'false')
        elif isinstance(curdef, string_types):
            newdef = val
        else:
            newdef = val.strip('\n').split('\n')

        opt['default'] = newdef

    # parse command line options, they will override config files options
    options = vars(parser.parse_args())

    src = options.pop('sourcedir')
    tgt = options.pop('targetdir')
    try:
        action = options.pop('action')
    except KeyError:
        sys.stdout.write('Argument error: you must select an action using one '
                         'of the "sync", "update" or "diff" options, or by'
                         'defining it in a %HOME%/.dirsync or local '
                         'dirsync.cfg file.\n')
        sys.exit(1)

    sync(src, tgt, action, **options)
