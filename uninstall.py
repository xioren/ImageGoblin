#!/usr/bin/env python3
from os import system as shell


# run this to remove the symlink created by install.py
# linux only
# run as sudo


shell(f'rm /usr/local/bin/goblin')
