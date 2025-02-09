import os

from time import sleep

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
