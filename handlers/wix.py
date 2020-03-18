import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class WixGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    url types:
        - image
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, tickrate, verbose, nodl)
        self.mode = mode
        print(f'[{self.__str__()}] <running>')

    def __str__(self):
        return 'wix goblin'

    def run(self):
        if self.mode == 'iter':
            links = self.read_file(self.external_links, True)
        else:
            links = [self.url]
        for link in links:
            self.loot(re.sub(r'\.jpg.+$', '', link) + '.jpg')
            sleep(self.tickrate)
