#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 mchristof <mchristof@Mikes-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""

"""

import re
import os
from sh import ansible_playbook
from sh import vagrant
from sh import tee
import json


def main():
    """docstring for main"""

    import argparse
    parser = argparse.ArgumentParser(
        description='Controls Shiny octo garbanzo through alfred')
    # subparsers = parser.add_subparsers(help='commands')

    parser.add_argument('-c', '--cmd',
                        help='Command to execute')

    args = parser.parse_args()

    cmd = {
        'on': 'cmd-power-on',
        'off': 'cmd-power-off',
    }
    if args.cmd is not None:
        if args.cmd.startswith(cmd['on']):
            from subprocess import call
            call(["vagrant", "up"])
            power_log = vagrant('up')
        elif args.cmd.startswith(cmd['off']):
            power_log = vagrant('suspend')
        with open('/tmp/vagrant-power.log', 'w') as stream:
            stream.write(str(power_log))
        return

    items = []
    try:
        items += get_urls()
    except:
        items += [{
            'title': 'Power on',
            'arg': cmd['on'],
            'icon': {
                'path': os.path.abspath('icons/power_button.png')
            }
        }]

    items += [{
        'title': 'Power off',
        'arg': cmd['off'],
        'icon': {
            'path': os.path.abspath('icons/off.png')
        }
    }]

    ret = {
        'items': items,
    }
    print json.dumps(ret, indent=4)


def get_urls():
    for line in str(ansible_playbook('setup.yml',
                                     '-T', '1',
                                     '--tags', 'ip')).split('\n'):
        needle = re.search('external_ip": "(.*)"', line)
        if needle:
            ip = needle.group(1)

    return [
        {
            'title': 'Transmission',
            'arg': 'http://{}:9091'.format(ip),
            'icon': {
                'path': os.path.abspath('icons/transmission.png'),
            },
        },
        {
            'title': 'Sonarr',
            'arg': 'http://{}:8989'.format(ip),
            'icon': {
                'path': os.path.abspath('icons/sonarr.png'),
            },
        }
    ]


if __name__ == '__main__':
    main()
