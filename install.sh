#!/bin/bash


# run this after placing the program directory in the location you want it
# linux only
# run as sudo
# pass u to uninstall


if [ $1 == 'u' ]
then
    rm /usr/local/bin/goblin
else
    ln -s $PWD/image_goblin/image_goblin.py /usr/local/bin/goblin
fi
