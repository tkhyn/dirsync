import pytest

from base import DirSyncTests
import trees

from dirsync import sync


class TestsUpdateWithDst(DirSyncTests):

    init_trees = (('src', trees.simple),)

    @pytest.fixture(autouse=True)
    def sync_create(self, tree):
        sync('src', 'dst', 'sync', create=True)

    def test_del_src_dir(self):
        self.rm('src/dir')

        sync('src', 'dst', 'update')

        self.assertNotExists('src/dir')
        self.assertExists('dst/dir')
