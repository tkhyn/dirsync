import os

from dirsync import sync

from .base import DirSyncTestCase
from . import trees


class SyncTestsFromSrc(DirSyncTestCase):

    init_trees = (('src', trees.simple), )

    def test_sync_all(self):
        sync('src', 'dst',
             action='sync',
             create=True)

        self.assertIsFile('dst/file1.txt')
        self.assertIsDir('dst/dir')
        self.assertListDir('dst/dir', ['file4.txt'])
        self.assertIsDir('dst/empty_dir')
        self.assertListDir('dst/empty_dir', [])

    def test_sync_modif(self):
        sync('src', 'dst',
             action='sync',
             create=True)

        file1 = open('src/file1.txt', 'r+')
        file1.write('modifying file')
        file1.close()

        result = sync('src', 'dst',
                      action='sync',
                      create=True)

        self.assertSetEqual(result, set([os.path.join('dst', 'file1.txt')]))
        file1 = open('dst/file1.txt', 'r')
        self.assertEqual(file1.read(), 'modifying file')
        file1.close()

