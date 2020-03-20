import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class MissguidedGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    url types:
        - image
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        self.mode = mode
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'missguided goblin'

    def extract(self, url):
        return re.search(r'[A-Z\d]+', url).group().upper()

    def run(self):
        id = self.extract(self.url)
        for n in range(1, 6):
            self.loot(f'https://media.missguided.com/i/missguided/{id}_0{n}')
            sleep(self.tickrate)
