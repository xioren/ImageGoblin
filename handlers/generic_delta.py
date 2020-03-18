import re
from time import sleep
from parsing import *
from handlers.meta_goblin import MetaGoblin


class DeltaGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    url types:
        - image
    generic backend for:
        - bershka
        - oysho
        - pull and bear
        - stradivarius
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, tickrate, verbose, nodl)
        self.mode = mode
        self.ids = ('_1_1_', '_2_1_', '_2_2_', '_2_3_',
                    '_2_4_', '_2_5_', '_2_6_', '_2_7_',
                    '_2_8_', '_2_9_', '_4_1_', '_6_1_')

    def clean(url):
        return re.sub(r'&imwidth=\d+', '', url)

    def run(url: 'image url', override=None):
        if self.mode == 'iter':
            links = self.read_file(self.external_links, True)
        else:
            links = [self.url]
        for link in links:
            base, end = re.split(r'_\d_\d_\d+', link)
            for id in ids:
                self.loot(f'{base}{id}{self.size}{self.clean(end)}')
                sleep(self.tickrate)
