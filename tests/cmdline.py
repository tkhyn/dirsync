"""
Command line options tests
"""

from dirsync.options import ArgParser
from dirsync.run import sync

from .base import DirSyncTestCase
from . import trees


class CmdLineTests(DirSyncTestCase):

    parser = ArgParser()

    def dirsync(self, *args):
        sync(**vars(self.parser.parse_args(args)))


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
