#!/usr/bin/env python3
"""
Downloads the libraries as zip files from github and unzips them.
"""

import os
import shutil
import zipfile

import wget

from duino import common


def main():
    """Creates the markdown for the README.md table."""
    args = common.parse_args()
    common.create_dir_if_needed(common.LIBRARIES_DIR)
    for key in common.get_names():
        zip_url = common.ZIP_URL.format(name=key, branch=common.BRANCH_NAME)
        if common.is_lib(key):
            extract_dir = common.LIBRARIES_DIR
        else:
            extract_dir = '.'

        print(f'Downloading {zip_url} ...')
        # Download the zipfile
        # wget.__current_size = 0
        filename = wget.download(zip_url, bar=None)

        extracted_dir = os.path.join(extract_dir,
                                     f'{key}-{common.BRANCH_NAME}')
        final_dir = os.path.join(extract_dir, f'{key}')

        print(f'  Extracting {filename} to {extracted_dir} ...')
        # Extract the files from the zipfile
        with zipfile.ZipFile(filename, 'r') as zip_f:
            zip_f.extractall(extract_dir)

        if args.force and os.path.exists(final_dir):
            print(f'  Removing {final_dir} ...')
            shutil.rmtree(final_dir)

        # Rename the directory
        print(f'  Renaming {extracted_dir} to {final_dir} ...')
        os.rename(extracted_dir, final_dir)

        # Remove the downloaded zip file
        print(f'  Removing {filename} ...')
        os.remove(filename)


if __name__ == '__main__':
    main()
