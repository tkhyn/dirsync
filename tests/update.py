from .base import DirSyncTestCase
from . import trees

from dirsync import sync


class UpdateTestsWithDst(DirSyncTestCase):

    init_trees = (('src', trees.simple),)

    def setUp(self):
        super(UpdateTestsWithDst, self).setUp()
        sync('src', 'dst', action='sync', create=True)

    def test_del_src_dir(self):
        self.rm('src/dir')

        sync('src', 'dst', action='update')

        self.assertNotExists('src/dir')
        self.assertExists('dst/dir')
