"""
Setup file for the duino_vscode_settings module.
"""

from pathlib import Path
import sys

from setuptools import setup
from duino.version import __version__

if sys.version_info < (3, 9):
    print('duino requires Python 3.9 or newer.')
    sys.exit(1)

here = Path(__file__).parent
long_description = (here / "README.md").read_text()

setup(
    name='duino',
    version=__version__,
    author='Dave Hylands',
    author_email='dhylands@gmail.com',
    description=('Scripts for installing duino libraries.'),
    license='MIT',
    keywords='cmd cli arduino',
    url='https://github.com/dhylands/duino',
    download_url=
    f'https://github.com/dhylands/duino/shell/tarball/v{__version__}',
    packages=['duino'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: System :: Shells',
        'Topic :: Terminals :: Serial',
        'Topic :: Utilities',
    ],
    install_requires=[
        'duino_cli',
        'duino_bus',
        'duino_littlefs',
        'gitpython',
        'wget',
    ],
    entry_points={
        'console_scripts': [
            'install-duino-from-zip=duino.duino_install_from_zip:main'
            'install-duino-from-git=duino.duino_install_from_git:main'
        ],
    },
)
