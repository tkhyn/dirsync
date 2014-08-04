import os
import shutil

from six import string_types

try:
    import unittest2 as unittest
except ImportError:
    import unittest

__test__ = False
__unittest__ = True


class DirSyncTestCase(unittest.TestCase):
    """
    Base class for sync tests

    The setUp method creates the trees specified in init_trees
    The tearDown method cleans up the sandbox directory

    Be sure to call super() if you override them
    """

    init_trees = ()

    def setUp(self):
        for x in self.init_trees:
            self.mk_tree(*x)

    def tearDown(self):
        for x in os.listdir('.'):
            if os.path.isfile(x):
                os.remove(x)
            else:
                # using absolute path seems to prevent windows error
                # with python 2.7.2
                shutil.rmtree(os.path.join(os.getcwd(), x))

    def mk_tree(self, name, structure=()):
        cwd = os.getcwd()
        try:
            os.mkdir(name)  # raises an exception if dir exists, that's fine
            os.chdir(name)

            for x in structure:
                if isinstance(x, string_types):
                    open(x, 'w').close()  # create empty file
                else:
                    self.mk_tree(*x)
        finally:
            os.chdir(cwd)

    def rm(self, path):
        """Removes a directory or a file"""
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    def assertExists(self, path, msg=None):
        if not os.path.exists(path):
            standardMsg = '%s does not exist' % path
            self.fail(self._formatMessage(msg, standardMsg))

    def assertNotExists(self, path, msg=None):
        if os.path.exists(path):
            standardMsg = '%s exists' % path
            self.fail(self._formatMessage(msg, standardMsg))

    def assertIsFile(self, path, msg=None):
        self.assertExists(path, msg)
        if not os.path.isfile(path):
            standardMsg = '%s is not a file' % path
            self.fail(self._formatMessage(msg, standardMsg))

    def assertIsDir(self, path, msg=None):
        self.assertExists(path, msg)
        if not os.path.isdir(path):
            standardMsg = '%s is not a directory' % path
            self.fail(self._formatMessage(msg, standardMsg))

    def assertListDir(self, path, lst, msg=None):
        self.assertExists(path, msg)
        self.assertListEqual(os.listdir(path), lst)
