#!/usr/bin/env python3
from os import system as shell, getcwd


# run this after placing the program directory in the location you want it
# linux only
# run as sudo


shell(f'ln -s {getcwd()}/image_goblin/image_goblin.py /usr/local/bin/goblin')
