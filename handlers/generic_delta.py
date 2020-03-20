import re
from time import sleep
from parsing import *
from handlers.meta_goblin import MetaGoblin


class DeltaGoblin(MetaGoblin):

    '''
    for _n_n_n variants
    mode options:
        - iter: for multiple links (using external links file)
    url types:
        - image
        - webpage
    generic backend for:
        - bershka
        - massimodutti
        - oysho
        - pull and bear
        - stradivarius
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        self.mode = mode
        self.ids = ('_1_1_', '_2_1_', '_2_2_', '_2_3_',
                    '_2_4_', '_2_5_', '_2_6_', '_2_7_',
                    '_2_8_', '_2_9_', '_4_1_', '_6_1_')

    def clean(self, url):
        return re.sub(r'&imwidth=\d+', '', url)

    def run(self):
        if '.jpg' in self.url:
            links = [self.url]
        else:
            links = {l.group() for l in re.finditer(r'https*://static[^"]+\.jpe*g', self.get_html(self.url))}
        for link in links:
            base, end = re.split(r'_\d_\d_\d+', link)
            for id in self.ids:
                self.loot(f'{base}{id}{self.size}{self.clean(end)}')
                sleep(self.tickrate)
