#!/bin/bash

# linux only
# run this after placing the program in the desired location
# run with sudo
# pass u to uninstall


if [ $1 ] && [ $1 == 'u' ]
then
    rm /usr/local/bin/image-goblin && echo symlink removed
else
    ln -s "$PWD"/image_goblin/image_goblin.py /usr/local/bin/image-goblin && echo symlink created at /usr/local/bin/image-goblin
fi
