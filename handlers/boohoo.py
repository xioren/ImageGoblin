import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class BoohooGoblin(MetaGoblin):

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
        return 'boohoo goblin'

    def extract_id(self, url):
        return re.search(r'\w+_\w+_xl', url).group()

    def run(self):
        if self.mode == 'iter':
            links = self.read_file(self.external_links, True)
        else:
            links = [self.url]
        for link in links:
            id = self.extract_id(link)
            self.loot(f'https://i1.adis.ws/i/boohooamplience/{id}', self.path_main)
            sleep(self.tickrate)
            for n in range(1, 6):
                self.retrieve(f'https://i1.adis.ws/i/boohooamplience/{id}_{n}', self.path_main)
                sleep(self.tickrate)
