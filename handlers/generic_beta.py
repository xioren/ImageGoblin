import re
from time import sleep
from parsing import *
from handlers.meta_goblin import MetaGoblin


class BetaGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    url types:
        - image
    generic backend for:
        - calvin klein
        - free people
        - hot topic
        - tommy hilfiger
        - urban outfitters
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, tickrate, verbose, nodl)
        self.mode = mode

    def extract_id(self, url):
        return re.search(r'\w+_\d+', url).group()

    def run(self):
        if self.mode == 'iter':
            links = self.read_file(self.external_links, True)
        else:
            links = [self.url]
        for link in links:
            base, query = self.identify(link)
            id = self.extract_id(link)
            for char in self.chars:
                self.loot(f'{base}{id}_{char}{query}')
                sleep(self.tickrate)
