import os
import shutil
import logging

from six import string_types, StringIO

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
            self.rm(x)

        # cleanup dirsync logger
        log = logging.getLogger('dirsync')
        for hdl in log.handlers:
            log.removeHandler(hdl)

        # cleanup test log stream
        log_stream = getattr(self, '_log_stream', None)
        if log_stream:
            log_stream.close()

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

    @property
    def logger(self):
        """Creates a test logger for output analysis"""
        logger = getattr(self, '_logger', None)
        if logger:
            return logger
        self._logger = logging.getLogger('dirsync_test')
        self._logger.setLevel(logging.INFO)
        for h in self._logger.handlers:
            self._logger.removeHandler(h)
        self._log_stream = StringIO()
        hdl = logging.StreamHandler(self._log_stream)
        hdl.setFormatter(logging.Formatter('%(message)s'))
        self._logger.addHandler(hdl)
        return self._logger

    @property
    def output(self):
        """Retrieves the logging output"""
        return self._log_stream.getvalue()

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
