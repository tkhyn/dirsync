"""
dirsync's functions
"""

import sys

from .syncer import Syncer


def sync(src_dir, tgt_dir, action, **options):

    copier = Syncer(src_dir, tgt_dir, action=action, **options)
    copier.do_work()

    # print report at the end
    copier.report()

    return set(copier._changed).union(copier._added).union(copier._deleted)


def execute_from_command_line():
    import argparse
    from .options import options

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

    for opt, args in options:
        parser.add_argument('--' + opt, *args[0], **args[1])

    options = vars(parser.parse_args())

    src = options.pop('sourcedir')
    tgt = options.pop('targetdir')
    try:
        action = options.pop('action')
    except KeyError:
        sys.stdout.write('Argument error: you must select an action using one '
                         'of the "sync", "update" or "diff" options\n')
        sys.exit(1)

    sync(src, tgt, action, **options)
