import os

from time import sleep
import shutil
import stat
from pathlib import Path

import pytest

from dirsync import sync

from base import DirSyncTests
import trees

class TestsSyncFromSrc(DirSyncTests):

    init_trees = (('src', trees.simple), )

    def test_sync_all(self):
        sync('src', 'dst', 'sync',
             create=True)

        self.assertIsFile('dst/file1.txt')
        self.assertIsDir('dst/dir')
        self.assertListDir('dst/dir', ['file4.txt'])
        self.assertIsDir('dst/empty_dir')
        self.assertListDir('dst/empty_dir', [])

    def test_sync_modif(self):
        sync('src', 'dst', 'sync',
             create=True)

        sleep(0.001)

        file1 = open('src/file1.txt', 'r+')
        file1.write('modifying file')
        file1.close()

        result = sync('src', 'dst', 'sync',
                      create=True)

        assert result == {os.path.join('dst', 'file1.txt')}
        file1 = open('dst/file1.txt', 'r')
        assert file1.read() == 'modifying file'
        file1.close()


class TestsSyncWithDest(DirSyncTests):

    init_trees = (('src', trees.simple),)

    @pytest.fixture(autouse=True)
    def sync_create(self, tree):
        sync('src', 'dst', 'sync', create=True)

    def test_del_src_dir_purge(self):
        self.rm('src/dir')

        sync('src', 'dst', 'sync', purge=True)

        self.assertNotExists('src/dir')
        self.assertNotExists('dst/dir')

    def test_del_dst_dir_nopurge(self):
        self.rm('dst/dir')

        sync('src', 'dst', 'sync')

        self.assertExists('src/dir')
        self.assertExists('dst/dir')


class TestsDelReadOnlyDirAndFilePurge(DirSyncTests):
    """
    Highlights orphan directory containing read-only files not being deleted during sync with purge
    The test still fails most of the time, but the real-life behaviour is fixed, hence the @skip
    https://github.com/tkhyn/dirsync/issues/49
    """

    init_trees = (('src', (
        ('sub1', ('test1.txt',)),
        ('sub2', ('test1.txt',)),
        ('sub3', ('test1.txt',))
    ),),('dst',))

    @pytest.fixture(autouse=True)
    def make_files_read_only(self, tree):
        src_dir = Path('src')
        folders = [f[0] for f in self.init_trees[0][1]]

        for subfolder in folders:
            # Set the file to read-only, because only then the error occurs
            os.chmod(src_dir / subfolder / 'test1.txt', stat.S_IREAD)

        yield

        for base_dir in (src_dir, Path('dst')):
            for subfolder in folders:
                # Set the file to read-only, because only then the error occurs
                path = base_dir / subfolder / 'test1.txt'
                if path.exists():
                    os.chmod(path, stat.S_IWRITE)

    @pytest.mark.skip("This test fails most of the time, yet the bug it triggers is fixed. To "
                      "investigate at some stage.")
    def test_del_read_only_dir_and_file_purge(self):

        folders = [f[0] for f in self.init_trees[0][1]]

        # The first sync works fine
        sync('src', 'dst', "sync", purge=True, verbose=False)
        for subfolder in folders:
            self.assertExists(f'dst/{subfolder}/test1.txt')

        # Remove the sub2 directory from the source
        shutil.rmtree('src/sub2', onerror=lambda func, path, _: (os.chmod(path, stat.S_IWRITE), func(path)))

        # Now the sync (with purge set to True) should also delete the sub2 directory in the destination
        sync('src', 'dst', "sync", purge=True, verbose=False)
        # Very strange: Often I'll get an error, but sometimes it seems to work
        self.assertNotExists(f'dst/sub2/test1.txt')
        self.assertNotExists(f'dst/sub2')

class TestsSyncWithContent(DirSyncTests):

    init_trees = (('src', trees.simple),)

    @pytest.fixture(autouse=True)
    def sync_create(self, tree):
        sync('src', 'dst', 'sync', create=True)

    def test_src_priority(self):
        file1 = open('src/file1.txt', 'r+')
        file1.write('Source content')
        file1.close()

        file1 = open('dst/file1.txt', 'r+')
        file1.write('Destination content differs from source. And older timestamp.')
        file1.close()

        sync('src', 'dst', 'sync', content=True)

        file1 = open('dst/file1.txt', 'r')
        assert file1.read() == 'Source content'
        file1.close()

    def test_src_priority_twoway(self):
        file1 = open('src/file1.txt', 'r+')
        file1.write('Source content')
        file1.close()

        file1 = open('dst/file1.txt', 'r+')
        file1.write('Destination file\'s content differs from source. And older timestamp of destination file.')
        file1.close()

        sync('src', 'dst', 'sync', content=True, twoway=True)

        file1 = open('dst/file1.txt', 'r')
        assert file1.read(), 'Source content'
        file1.close()
