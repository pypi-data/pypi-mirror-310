#!/usr/bin/env python3
"""
Downloads the libraries as zip files from github and unzips them.
"""

import os
import shutil

from git import Repo

from duino import common


def main():
    """Creates the markdown for the README.md table."""
    args = common.parse_args()
    common.create_dir_if_needed(common.LIBRARIES_DIR)
    for key in common.get_names():
        if common.is_lib(key):
            repo_dir = os.path.join(common.LIBRARIES_DIR, key)
        else:
            repo_dir = os.path.join('.', key)

        if args.force and os.path.exists(repo_dir):
            print(f'  Removing {repo_dir} ...')
            shutil.rmtree(repo_dir)

        git_url = common.get_repo_url(key)
        print(f'git cloning {git_url} into {repo_dir} ...')

        Repo.clone_from(git_url, repo_dir)


if __name__ == '__main__':
    main()
