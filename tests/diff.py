import os

from .base import DirSyncTestCase
from . import trees

from dirsync import sync


class DiffTests(DirSyncTestCase):

    init_trees = (('src', trees.simple),)

    def setUp(self):
        super(DiffTests, self).setUp()
        sync('src', 'dst', 'sync', create=True)

    def test_del_src_dir(self):
        self.rm('src/dir')

        sync('src', 'dst', 'diff', logger=self.logger)

        self.assertListEqual(self.output.splitlines()[:11],
            ['Difference of directory dst from src',
             '',
             'Only in dst',
             '<< dir',
             '<< dir%sfile4.txt' % os.sep,
             '',
             'Common to src and dst',
             '-- empty_dir',
             '-- file1.txt',
             '-- file2.py',
             '-- file3.js'])
