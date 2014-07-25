from base import SyncTestCase
import trees

from dirsync import sync


class SimpleTests(SyncTestCase):

    init_trees = (('src', trees.simple),)

    def test_simple_exclude(self):
        sync('src', 'dst',
             action='sync',
             create=True,
             exclude=('^dir.*$',
                      '^.*\.py$'))

        self.assertNotExists('dst/file2.py')
        self.assertNotExists('dst/dir')

    def test_exclude_include(self):
        sync('src', 'dst',
             action='sync',
             create=True,
             exclude=('^.*\.py$',),
             include=('^file2\.py$',))

        self.assertExists('dst/file2.py')

    def test_exclude_include_ignore(self):
        sync('src', 'dst',
             action='sync',
             create=True,
             exclude=('^.*\.py$',),
             ignore=('^.*\.txt$',),
             include=('^file2\.py$',))

        self.assertNotExists('dst/file1.txt')
        self.assertNotExists('dst/dir/file4.txt')


class PyprojTests(SyncTestCase):

    init_trees = (('src', trees.pyproj),)

    def test_real_life(self):
        sync('src', 'dst',
            action='sync',
            purge=True,
            create=True,
            modtime=True,
            exclude=(r'.*\.pyc',
                     r'^fab.*\.py$',
                     # any dir or file name starting with _ or .
                     r'^(?:.*[\\/])?[_.][^_].*$',
                     r'(?i).*/thumbs.db'),
            ignore=(r'^settings/local.py$',
                    r'^static/.*\.css$',
                    r'^.*\.min.js$'),
            include=(r'^_buildout/parts.cfg',)
        )

        self.assertNotExists('dst/.hg')
        self.assertNotExists('dst/.hiddendir')
        self.assertNotExists('dst/_ignoredir')
        self.assertExists('dst/_buildout/parts.cfg')
        self.assertExists('dst/cpnts/base/__init__.py')
        self.assertNotExists('dst/cpnts/base/__init__.pyc')
        self.assertExists('dst/cpnts/app/__init__.py')
        self.assertNotExists('dst/cpnts/app/__init__.pyc')
        self.assertNotExists('dst/settings/local.py')
        self.assertExists('dst/settings/local.py.sample')

        self.assertNotExists('dst/static/_scss')
        self.assertExists('dst/static/css')
        self.assertNotExists('dst/static/css/file.css')
        self.assertExists('dst/static/img')
        self.assertNotExists('dst/static/img/Thumbs.db')
        self.assertExists('dst/static/js/file.js')
        self.assertNotExists('dst/static/js/file.min.js')
        self.assertNotExists('fabfile.py')
        self.assertNotExists('fabfile.pyc')
