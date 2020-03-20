import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class VictoriasSecretGoblin(MetaGoblin):

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
        return 'victorias secret goblin'

    def extract(self, link):
        return re.search(r'\w+.jpg', link).group()

    def run(self):
        # TODO: add link dragnet
        self.loot(re.sub(r'\d+x\d+', '4040x5390', self.url))
        sleep(self.tickrate)
