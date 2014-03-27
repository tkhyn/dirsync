"""
dir-sync
Advanced directory tree synchronisation tool
(c) 2014 Thomas Khyn
MIT license (see LICENSE.txt)
"""

from distutils.core import setup
import os

INC_PACKAGES = 'dirsync',  # string or tuple of strings
EXC_PACKAGES = ()  # tuple of strings

install_requires = (
)

# imports __version__ and __version_info__ variables
exec(open('dirsync/version.py').read())

dev_status = __version_info__[3]
if dev_status == 'alpha' and not __version_info__[4]:
    dev_status = 'pre'

DEV_STATUS = {'pre': '2 - Pre-Alpha',
              'alpha': '3 - Alpha',
              'beta': '4 - Beta',
              'rc': '5 - Production/Stable',
              'final': '5 - Production/Stable'}

# setup function parameters
metadata = dict(
    name='dir-sync',
    version=__version__,
    description='Advanced directory tree synchronisation tool',
    author='Thomas Khyn',
    author_email='thomas@ksytek.com',
    url='http://open.ksytek.com/dir-sync/',  # TODO: check url
    keywords=['directory', 'folder', 'update', 'synchronisation'],
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: %s' % DEV_STATUS[dev_status],
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console',
        'Topic :: Utilities',
        'Topic :: Desktop Environment',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: Desktop Environment :: Mirroring'
    ]
)


# packages parsing from root packages, without importing sub-packages
root_path = os.path.dirname(__file__)
if isinstance(INC_PACKAGES, basestring):
    INC_PACKAGES = (INC_PACKAGES,)

packages = []
excludes = list(EXC_PACKAGES)
for pkg in INC_PACKAGES:
    pkg_root = os.path.join(root_path, *pkg.split('.'))
    for dirpath, dirs, files in os.walk(pkg_root):
        rel_path = os.path.relpath(dirpath, pkg_root)
        pkg_name = pkg
        if (rel_path != '.'):
            pkg_name += '.' + rel_path.replace(os.sep, '.')
        for x in excludes:
            if x in pkg_name:
                continue
        if '__init__.py' in files:
            packages.append(pkg_name)
        elif dirs:  # stops package parsing if no __init__.py file
            excludes.append(pkg_name)


def read(filename):
    return open(os.path.join(root_path, filename)).read()

setup(**dict(metadata,
   packages=packages,
   long_description=read('README.txt'),  # use reST in README.txt !
   install_requires=install_requires
))
