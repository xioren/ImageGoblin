import re
from time import sleep
from handlers.meta_goblin import MetaGoblin

# NOTE: can also use generic gamma, but might be lesser resolution

class HunkemollerGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    url types:
        - image
        - web page
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, tickrate, verbose, nodl)
        self.mode = mode
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'hunkemoller goblin'

    def run(self):
        id = re.search(r'(/|-)\d+', self.url).group().replace('/', '').replace('-', '')
        for num in range(1, 6):
            self.loot(f'https://images-hunkemoller.akamaized.net/original/{id}_{num}.jpg')
            sleep(self.tickrate)
