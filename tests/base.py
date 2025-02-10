import os
import shutil
import logging
import time
from io import StringIO
from unittest.util import safe_repr

import pytest

__test__ = False
__unittest__ = True



class DirSyncTests:
    """
    Base class for dirsync tests

    The tree fixture creates the trees specified in init_trees and cleans up the sandbox directory
    """

    init_trees = ()

    @pytest.fixture(autouse=True)
    def tree(self):
        for x in self.init_trees:
            self.mk_tree(*x)

        yield

        time.sleep(0.01)

        for x in os.listdir('.'):
            self.rm(x)

        # cleanup dirsync and test loggers
        loggers = [logging.getLogger('dirsync')]
        try:
            loggers.append(self._logger)
        except AttributeError:
            pass
        for logger in loggers:
            for hdl in logger.handlers:
                hdl.close()
                logger.removeHandler(hdl)

    def mk_tree(self, name, structure=()):
        cwd = os.getcwd()
        try:
            os.mkdir(name)  # raises an exception if dir exists, that's fine
            os.chdir(name)

            for x in structure:
                if isinstance(x, str):
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

    # from unittest.TestCase
    def formatMessage(self, msg, standardMsg):
        if msg is None:
            return standardMsg
        try:
            return '%s : %s' % (standardMsg, msg)
        except UnicodeDecodeError:
            return  '%s : %s' % (safe_repr(standardMsg), safe_repr(msg))


    def assertExists(self, path, msg=None):
        if not os.path.exists(path):
            standardMsg = '%s does not exist' % path
            pytest.fail(self.formatMessage(msg, standardMsg))

    def assertNotExists(self, path, msg=None):
        if os.path.exists(path):
            standardMsg = '%s exists' % path
            pytest.fail(self.formatMessage(msg, standardMsg))

    def assertIsFile(self, path, msg=None):
        self.assertExists(path, msg)
        if not os.path.isfile(path):
            standardMsg = '%s is not a file' % path
            pytest.fail(self.formatMessage(msg, standardMsg))

    def assertIsDir(self, path, msg=None):
        self.assertExists(path, msg)
        if not os.path.isdir(path):
            standardMsg = '%s is not a directory' % path
            pytest.fail(self.formatMessage(msg, standardMsg))

    def assertListDir(self, path, lst, msg=None):
        self.assertExists(path, msg)
        assert os.listdir(path) == lst
