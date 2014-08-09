"""
Command line options tests
"""

from six import iteritems

from dirsync.options import ArgParser
from dirsync.run import sync

from .base import DirSyncTestCase
from . import trees


class CmdLineTests(DirSyncTestCase):

    def dirsync(self, *args):
        sync(**vars(ArgParser().parse_args(args)))


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


class CfgFiles(CmdLineTests):

    init_trees = (('src', trees.simple),)

    def mk_cfg_file(self, **options):
        cfg_file = open('dirsync.cfg', 'w')
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
