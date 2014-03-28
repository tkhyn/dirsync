
__test__ = False

# very basic tree
simple = (
    'file1.txt',
    'file2.py',
    'file3.js',
    ('empty_dir',),
    ('dir', ('file4.txt',))
)

# project-like tree
pyproj = (
    ('.hg', ('hgfile',)),
    ('.hiddendir', ('file',)),
    ('_ignoredir', ('file',)),
    ('_buildout', ('parts.cfg',)),
    ('cpnts', (('base', ('__init__.py',
                         '__init__.pyc')),
               ('app', ('__init__.py',
                        '__init__.pyc')))),
    ('settings', ('local.py',
                  'local.py.sample')),
    ('static', (('_scss', (('.sass-cache',),
                           'file.scss')),
                ('css', ('file.css',)),
                ('img', ('Thumbs.db',)),
                ('js', ('file.js',
                        'file.min.js')))),
    'fabfile.py',
    'fabfile.pyc',
)
