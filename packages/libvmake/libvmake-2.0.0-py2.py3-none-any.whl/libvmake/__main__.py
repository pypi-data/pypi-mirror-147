#!/usr/bin/env python3

# encoding: utf-8

# usage: save as __main__.py in your module, and then use by command `python -m libvmake <command>`

import sys
import os


def showhelp():
    print(f'''usage: {sys.executable} -m libvmake <action>
action is one of:
    help            show help document
''')

if __name__ == "__main__":
    try:
        action = 'help' if sys.argv[1] == '-h' or sys.argv[1] == "--help" else sys.argv[1]
        if action not in ['help']:
            raise Exception("invalid parameter")
    except:
        print("invalid parameter, use -h to view help", file=sys.stderr)
        sys.exit(1)

    if action == "help":
        showhelp()
    else:
        print("invalid parameter, use -h to view help", file=sys.stderr)
        sys.exit(1)