"""
Common functions.
"""

import argparse
import os
import sys
from typing import List

from duino.libs import LIBS

GIT_URL = 'https://github.com/dhylands/{name}'
ACTIONS_URL = GIT_URL + '/actions'
BADGE_URL = ACTIONS_URL + '/workflows/build.yml/badge.svg'
BRANCH_NAME = 'main'
ZIP_URL = GIT_URL + '/archive/refs/heads/{branch}.zip'
LIBRARIES_DIR = 'libraries'


def get_names() -> List[str]:
    """Returns a sorted list of libraries."""
    return sorted(LIBS.keys())


def get_repo_url(name: str) -> str:
    """Returns the git repo URL given the repo name."""
    return GIT_URL.format(name=name)


def get_description(name: str) -> str:
    """Returns the description given the repo name."""
    if name in LIBS:
        lib = LIBS[name]
        if 'description' in lib:
            return lib['description']
    return ''


def get_badge_url(name: str) -> str:
    """Returns the URL of the Badge image, given the repo name."""
    return BADGE_URL.format(name=name)


def get_actions_url(name: str) -> str:
    """Returns the URL to see the actions given the repo name."""
    return ACTIONS_URL.format(name=name)


def has_badge(name: str) -> bool:
    """Returns True if the repo given by name has an action badge."""
    if name in LIBS:
        lib = LIBS[name]
        if 'has_badge' in lib:
            return lib['has_badge']
        return True
    return False


def is_lib(name: str) -> bool:
    """Returns True if the repo given by name is a library."""
    if name in LIBS:
        lib = LIBS[name]
        if 'is_lib' in lib:
            return lib['is_lib']
        return True
    return False


def create_dir_if_needed(dirname: str) -> None:
    """Creates a directory, if it doesn't exist already."""
    if os.path.exists(dirname):
        if os.path.isdir(dirname):
            return
        raise ValueError(f'{dirname} isn\'t a directory')
    print(f'Creating {dirname}')
    os.mkdir(dirname)


def parse_args() -> argparse.Namespace:
    """Parses the command line arguments."""
    parser = argparse.ArgumentParser(
        usage='%(prog)s [options]',
        description='Downloads and extracts duino zipfiles.',
    )
    parser.add_argument(
        '-f',
        '--force',
        action='store_true',
        help='Overwrite directories.',
        default=False,
    )
    return parser.parse_args(sys.argv[1:])
