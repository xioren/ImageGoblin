import re
import os
from time import sleep
from handlers.meta_goblin import MetaGoblin


class AlphaGoblin(MetaGoblin):

    '''
    for: media/catalog variants
    mode options:
        - iter: for multiple links (using external links file)
    format option:
        - clean: decrop image
    url types:
        - webpage
    back-end for:
        - agent provocateur
        - blush
        - maison close
        - only hearts
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, tickrate, verbose, nodl)
        self.mode = mode
        self.image_pat = r'https*\:[^" \n]+media(\\)*/catalog[^" \n]+\.jpe*g'

    def upgrade(self, path, base):
        '''
        upgrade existing files
        '''
        # NOTE: unused
        base = base.rstrip('/')
        for file in os.listdir(path):
            file = re.sub(r'\.(jpe*g|png)', '', file)
            self.loot(f'{base}/media/catalog/product/{file[0]}/{file[1]}/{file}.jpg')
            sleep(self.tickrate)

    def run(self):
        if '.jpg' in self.url:
            # QUESTION: possible?
            pass
        else:
            parsed_links = re.finditer(self.image_pat, self.get_html(self.url))
            for parsed in {p.group() for p in parsed_links}:
                self.loot(re.sub(r'cache/(\d/\w+/(\d+x(\d+)*/)*)*\w+/', '', parsed.replace('\\', '')), clean=True)
                sleep(self.tickrate)
