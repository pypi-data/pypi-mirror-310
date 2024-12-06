#!/usr/bin/env python3
"""
Creates the markdown for the README.md table.
"""

from duino import common


def main():
    """Creates the markdown for the README.md table."""
    for key in common.get_names():
        repo = common.get_repo_url(key)
        descr = common.get_description(key)
        if common.has_badge(key):
            badge_url = common.get_badge_url(key)
            actions_url = common.get_actions_url(key)
            badge = f'[<img src="{badge_url}">]({actions_url})'
        else:
            badge = ''

        print(f'| [{key}]({repo}) | {descr} | {badge} |')


if __name__ == '__main__':
    main()
