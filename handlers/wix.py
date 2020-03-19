import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class WixGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    url types:
        - image
    # TODO: add web page?
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, tickrate, verbose, nodl)
        self.mode = mode
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'wix goblin'

    def run(self):
        self.loot(re.sub(r'\.jpg.+$', '', self.url) + '.jpg')
        sleep(self.tickrate)
