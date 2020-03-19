import re
from time import sleep
from parsing import *
from handlers.meta_goblin import MetaGoblin


class SavageXGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    link types:
        - web page
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, tickrate, verbose, nodl)
        self.mode = mode
        self.image_pat = r'https*://[^" \n]+800x800.jpg'
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'savagex goblin'

    def run(self):
        parsed_links = re.finditer(self.image_pat, self.get_html(self.url))
        for parsed in {p.group() for p in parsed_links}:
            self.loot(parsed.replace('800x800', '1600x1600'))
            sleep(self.tickrate)
        self.cleanup(self.path_main)
