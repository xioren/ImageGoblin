#!/bin/bash


# run this after placing the program in the location you want it
# linux only
# run with sudo
# pass u to uninstall


if [ $1 ] && [ $1 == 'u' ]
then
    rm /usr/local/bin/goblin && echo symlink removed
else
    ln -s "$PWD"/image_goblin/image_goblin.py /usr/local/bin/goblin && echo symlink created at /usr/local/bin/goblin
fi
