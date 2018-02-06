"""
Command line options tests
"""

import os
import re

from six import iteritems, StringIO
try:
    # Python 3
    from unittest.mock import patch
except ImportError:
    from mock import patch

from dirsync.options import ArgParser
from dirsync.run import sync

from ._base import DirSyncTestCase
from . import trees


class CmdLineTests(DirSyncTestCase):

    def dirsync(self, *args, **kwargs):
        kwargs.update(vars(ArgParser().parse_args(args)))
        sync(**kwargs)


class SyncTests(CmdLineTests):

    init_trees = (('src', trees.simple),)

    def test_sync(self):
        self.dirsync('src', 'dst', '--sync', '-c')

        self.assertIsFile('dst/file1.txt')
        self.assertIsDir('dst/dir')
        self.assertListDir('dst/dir', ['file4.txt'])
        self.assertIsDir('dst/empty_dir')
        self.assertListDir('dst/empty_dir', [])

    def test_no_action(self):
        with self.assertRaises(ValueError):
            self.dirsync('src', 'dst')

    def test_no_create(self):
        with self.assertRaises(ValueError):
            self.dirsync('src', 'dst', '--sync')

    @patch('sys.stdout', new_callable=StringIO)
    def test_output(self, stdout):
        self.dirsync('src', 'dst', '--sync', '-c')
        self.dirsync('src', 'dst', '--sync', '-c')

        self.assertEqual(
            re.sub('\d\.\d{2}', 'X', stdout.getvalue().strip()),
            'dirsync finished in X seconds.\n'
            '3 directories parsed, 4 files copied\n'
            '3 directories were created.\n\n'
            'dirsync finished in X seconds.\n'
            '3 directories parsed, 0 files copied'
        )


class CfgFiles(CmdLineTests):

    init_trees = (('src', trees.simple),)

    def mk_cfg_file(self, **options):
        cfg_file = open(os.path.join('src', '.dirsync'), 'w')
        cfg_file.write('[defaults]\n')
        for opt, val in iteritems(options):
            cfg_file.write('%s = %s\n' % (opt, str(val)))
        cfg_file.close()

    def test_sync_default(self):
        self.mk_cfg_file(action='sync', create=True)

        self.dirsync('src', 'dst')

        self.assertIsFile('dst/file1.txt')
        self.assertIsDir('dst/dir')
        self.assertListDir('dst/dir', ['file4.txt'])
        self.assertIsDir('dst/empty_dir')
        self.assertListDir('dst/empty_dir', [])

        self.assertNotExists('dst/.dirsync')
