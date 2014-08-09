import os
import sys

try:
    from StringIO import StringIO  # py2.x
except ImportError:
    from io import StringIO  # py3.x

from .base import DirSyncTestCase
from . import trees

from dirsync import sync


class DiffTests(DirSyncTestCase):

    init_trees = (('src', trees.simple),)

    def setUp(self):
        super(DiffTests, self).setUp()
        sync('src', 'dst', 'sync', create=True)

        self.output = StringIO()
        self.saved_stdout = sys.stdout
        sys.stdout = self.output

    def tearDown(self):
        self.output.close()
        sys.stdout = self.saved_stdout
        super(DiffTests, self).tearDown()

    def test_del_src_dir(self):
        self.rm('src/dir')

        sync('src', 'dst', 'diff')

        self.assertListEqual(self.output.getvalue().splitlines()[:11],
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
