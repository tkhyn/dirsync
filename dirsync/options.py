"""
Dirsync options list
"""

import os
from collections import OrderedDict
from argparse import ArgumentParser
try:
    from ConfigParser import ConfigParser  # python 2
except ImportError:
    from configparser import ConfigParser  # python 3


from six import string_types, iteritems

__all__ = ['OPTIONS', 'ArgParser']


options = (
    ('verbose', (('-v',), dict(
        action='store_true',
        default=False,
        help='Provide verbose output'
    ))),
    ('diff', (('-d',), dict(
        action='store_const',
        dest='action',
        const='diff',
        default=False,
        help='Only report difference between sourcedir and targetdir'
    ))),
    ('sync', (('-s',), dict(
        action='store_const',
        dest='action',
        const='sync',
        default=False,
        help='Synchronize content between sourcedir and targetdir'
    ))),
    ('update', (('-u',), dict(
        action='store_const',
        dest='action',
        const='update',
        default=False,
        help='Update existing content between sourcedir and targetdir'
    ))),
    ('purge', (('-p',), dict(
        action='store_true',
        default=False,
        help='Purge files when synchronizing (does not purge by default)'
    ))),
    ('force', (('-f',), dict(
        action='store_true',
        default=False,
        help='Force copying of files, by trying to change file permissions'
    ))),
    ('nodirection', (('-n',), dict(
        action='store_true',
        default=False,
        help='Create target directory if it does not exist ' \
             '(By default, target directory should exist).'
    ))),
    ('create', (('-c',), dict(
        action='store_true',
        default=False,
        help='Only compare file\'s modification times for an update '\
             '(By default, compares source file\'s creation time also).'
    ))),
    ('modtime', (('-m',), dict(
        action='store_true',
        default=False,
        help='Update existing content between sourcedir and targetdir'
    ))),
    ('only', (('-o',), dict(
        action='store', nargs='+',
        default=[],
        help='Patterns to exclusively include (exclude every other)'
    ))),
    ('exclude', (('-e',), dict(
        action='store', nargs='+',
        default=[],
        help='Patterns to exclude'
    ))),
    ('include', (('-i',), dict(
        action='store', nargs='+',
        default=[],
        help='Patterns to include (with precedence over excludes)'
    ))),
    ('ignore', (('-x',), dict(
        action='store', nargs='+',
        default=[],
        help='Patterns to ignore (no action)'
    ))),
)


OPTIONS = OrderedDict(options)


class ArgParser(ArgumentParser):

    def __init__(self, *args, **kwargs):
        kwargs['description'] = \
            'Syncer: Command line directory diff, synchronization, ' \
            'update & copy\n' \
            'Authors: Anand Pillai (v1.0), Thomas Khyn (v2.x)'
        super(ArgParser, self).__init__(*args, **kwargs)

        self.add_argument('sourcedir',
                          action='store',
                          help='Source directory')
        self.add_argument('targetdir',
                          action='store',
                          help='Target directory')
        for opt, args in options:
            self.add_argument('--' + opt, *args[0], **args[1])

    def parse_args(self, args=None, namespace=None):
        self.load_cfg()
        parsed = super(ArgParser, self).parse_args(args, namespace)

        if parsed.action == False:
            raise ValueError('Argument error: you must select an action using '
                             'one of the "sync", "update" or "diff" options\n')

        return parsed

    def load_cfg(self):
        """
        Load defaults from configuration file:
         - from a current working directory dirsync.cfg file
         - and/or a %HOME%/.dirsync user config file
        """

        cfg_files = [os.path.join(os.getcwd(), 'dirsync.cfg')]
        home_dir = os.environ.get('HOME', None)
        if home_dir:
            # inserting in first position so that it can be overriden by
            # cwd config file
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

            opt[name] = newdef

        self.set_defaults(**opt)
