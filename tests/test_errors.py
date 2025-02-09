import pytest

from base import DirSyncTests
import trees

from dirsync import sync


class TestsErrors(DirSyncTests):

    init_trees = (('src', trees.simple), ('dst', trees.simple))

    def test_nonexistent_src(self):
        with pytest.raises(ValueError):
            sync('srcc', 'dst', 'sync', create=True)

    def test_nonexistent_dest(self):
        with pytest.raises(ValueError):
            sync('src', 'dstt', 'sync', create=False)
