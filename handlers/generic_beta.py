import re
from time import sleep
from parsing import *
from handlers.meta_goblin import MetaGoblin


class BetaGoblin(MetaGoblin):

    '''
    for scen7 variants
    mode options:
        - iter: for multiple links (using external links file)
    url types:
        - image
        - webpage
    generic backend for:
        - anthropologie
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
        if 'scene7' in self.url:
            pass
        else:
            self.url = re.search(r'\w+\.scene7[^" \n]+', self.get_html(self.url)).group()
        base, query = self.identify(self.url)
        id = self.extract_id(self.url)
        for char in self.chars:
            self.loot(f'{base}{id}_{char}{query}')
            sleep(self.tickrate)
