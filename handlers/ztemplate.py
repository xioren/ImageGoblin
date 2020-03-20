import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class Goblin(MetaGoblin):

    '''
    mode options:
        -
    accepts:
        - 
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        self.mode = mode
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return ' goblin'

    def run(self):
        self.loot(self.url)
        sleep(self.tickrate)
