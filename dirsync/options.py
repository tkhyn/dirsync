"""
Dirsync options list
"""

import os
import sys
from argparse import ArgumentParser

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

try:
    from ConfigParser import ConfigParser  # python 2
except ImportError:
    from configparser import ConfigParser  # python 3

from six import string_types


from .version import __pkg_name__

__all__ = ['USER_CFG_FILE', 'DEFAULT_USER_CFG', 'OPTIONS', 'ArgParser']

USER_CFG_FILE = '~/.%s' % __pkg_name__
DEFAULT_USER_CFG = """# %s default options
[defaults]
action = sync
""" % __pkg_name__


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
        help='Synchronize content from sourcedir to targetdir'
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
    ('twoway', (('-2',), dict(
        action='store_true',
        default=False,
        help='Update files in source directory from target'
             'directory (only updates target from source by default)'
    ))),
    ('create', (('-c',), dict(
        action='store_true',
        default=False,
        help='Synchronize files from target to source directory as well.'
    ))),
    ('ctime', ((), dict(
        action='store_true',
        default=False,
        help='Also takes into account the source file\'s creation time '
             '(Windows) or the source file\'s last metadata change (Unix)'
    ))),
    ('content', ((), dict(
        action='store_true',
        default=False,
        help='Takes into account ONLY content of files. Synchronize ONLY different files. '
             'At two-way synchronization source files content have priority if destination and source are existed'
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
            '%s: Command line directory diff, synchronization, ' \
            'update & copy\n' \
            'Authors: Anand Pillai (v1.0), Thomas Khyn (v2.x)' % __pkg_name__
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
        if args or len(sys.argv) > 1:
            # if no args nor sys.argv, we don't bother loading the config as
            # there are missing args and super().parse_args below will raise an
            # exception
            self.load_cfg(args[0] if args else sys.argv[1])
        parsed = super(ArgParser, self).parse_args(args, namespace)

        if parsed.action is False:
            raise ValueError('Argument error: you must select an action using '
                             'one of the "sync", "update" or "diff" options\n')

        return parsed

    def load_cfg(self, src_dir):
        """
        Load defaults from configuration file:
         - from the source/directory/.dirsync file (prioritary)
         - and/or a %HOME%/.dirsync user config file
        """

        # last files override previous ones
        cfg_files = [os.path.expanduser(USER_CFG_FILE),
                     os.path.abspath(os.path.join(src_dir, '.dirsync'))]

        cfg = ConfigParser()
        cfg.read(cfg_files)

        if not cfg.has_section('defaults'):
            return

        defaults = {}
        for name, val in cfg.items('defaults'):
            try:
                opt = OPTIONS[name][1]
            except KeyError:
                if name == 'action':
                    if val in OPTIONS:
                        defaults['action'] = val
                    else:
                        raise ValueError('Invalid value for "action" option '
                                         'in configuration file: %s' % val)
                continue

            curdef = opt.get('default', '')
            if isinstance(curdef, bool):
                newdef = val not in ('0', 'False', 'false')
            elif isinstance(curdef, string_types):
                newdef = val
            else:
                newdef = val.strip('\n').split('\n')

            defaults[name] = newdef

        self.set_defaults(**defaults)
