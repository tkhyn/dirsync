"""
dirsync
Advanced directory tree synchronisation tool
(c) 2014-2019 Thomas Khyn
(c) 2003-2015 Anand B Pillai
MIT license (see LICENSE.txt)
"""

from setuptools import setup, find_packages
import os

# imports __version__ and __version_info__ variables
exec(open('dirsync/version.py').read())

INC_PACKAGES = __pkg_name__,  # string or tuple of strings
EXC_PACKAGES = ()  # tuple of strings

dev_status = __version_info__[3]
if dev_status == 'alpha' and not __version_info__[4]:
    dev_status = 'pre'

DEV_STATUS = {'pre': '2 - Pre-Alpha',
              'alpha': '3 - Alpha',
              'beta': '4 - Beta',
              'rc': '4 - Beta',
              'final': '5 - Production/Stable'}

setup(
    name=__pkg_name__,
    version=__version__,
    description='Advanced directory tree synchronisation tool',
    long_description=open(os.path.join('README.rst')).read(),
    author='Thomas Khyn',
    author_email='thomas@ksytek.com',
    url='https://bitbucket.org/tkhyn/dirsync/',
    keywords=['directory', 'folder', 'update', 'synchronisation'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: %s' % DEV_STATUS[dev_status],
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console',
        'Topic :: Utilities',
        'Topic :: Desktop Environment',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: System :: Archiving :: Mirroring'
    ],
    packages=find_packages(),
    install_requires=('six',),
    entry_points={
        'console_scripts': [
            'dirsync = dirsync.run:from_cmdline'
        ],
    }
)
