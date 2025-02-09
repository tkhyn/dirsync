import os

import pytest

from base import DirSyncTests
import trees

from dirsync import sync


class TestsDiff(DirSyncTests):

    init_trees = (('src', trees.simple),)

    @pytest.fixture(autouse=True)
    def sync(self, tree):
        sync('src', 'dst', 'sync', create=True)
        yield

    def test_del_src_dir(self):
        self.rm('src/dir')

        sync('src', 'dst', 'diff', logger=self.logger)

        assert self.output.splitlines()[:10] == [
            'Difference of directory dst from src',
             'Only in dst',
             '<< dir',
             '<< dir%sfile4.txt' % os.sep,
             '',
             'Common to src and dst',
             '-- empty_dir',
             '-- file1.txt',
             '-- file2.py',
             '-- file3.js'
        ]
