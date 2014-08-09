"""
Dirsync options list
"""

options = (
    ('verbose', (('-v'), dict(
        action='store_true',
        default=False,
        help='Provide verbose output'
    ))),
    ('diff', (('-d'), dict(
        action='store_const',
        dest='action',
        const='diff',
        default=False,
        help='Only report difference between sourcedir and targetdir'
    ))),
    ('sync', (('-s'), dict(
        action='store_const',
        dest='action',
        const='sync',
        default=False,
        help='Synchronize content between sourcedir and targetdir'
    ))),
    ('update', (('-u'), dict(
        action='store_const',
        dest='action',
        const='update',
        default=False,
        help='Update existing content between sourcedir and targetdir'
    ))),
    ('purge', (('-p'), dict(
        action='store_true',
        default=False,
        help='Purge files when synchronizing (does not purge by default)'
    ))),
    ('force', (('-f'), dict(
        action='store_true',
        default=False,
        help='Force copying of files, by trying to change file permissions'
    ))),
    ('nodirection', (('-n'), dict(
        action='store_true',
        default=False,
        help='Create target directory if it does not exist ' \
             '(By default, target directory should exist).'
    ))),
    ('create', (('-c'), dict(
        action='store_true',
        default=False,
        help='Only compare file\'s modification times for an update '\
             '(By default, compares source file\'s creation time also).'
    ))),
    ('modtime', (('-m'), dict(
        action='store_true',
        default=False,
        help='Update existing content between sourcedir and targetdir'
    ))),
    ('only', (('-o'), dict(
        action='store', nargs='+',
        default=[],
        help='Patterns to exclusively include (exclude every other)'
    ))),
    ('exclude', (('-e'), dict(
        action='store', nargs='+',
        default=[],
        help='Patterns to exclude'
    ))),
    ('include', (('-i'), dict(
        action='store', nargs='+',
        default=[],
        help='Patterns to include (with precedence over excludes)'
    ))),
    ('ignore', (('-x'), dict(
        action='store', nargs='+',
        default=[],
        help='Patterns to ignore (no action)'
    ))),
)
