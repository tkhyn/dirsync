from base import SyncTestCase
import trees

from dir_sync import sync


class SyncTests(SyncTestCase):

    init_trees = (('src', trees.simple),)

    def test_sync_all(self):
        sync('src', 'dst',
             action='sync',
             create=True)

        self.assertIsFile('dst/file1.txt')
        self.assertIsDir('dst/dir')
        self.assertListDir('dst/dir', ['file4.txt'])
        self.assertIsDir('dst/empty_dir')
        self.assertListDir('dst/empty_dir', [])
