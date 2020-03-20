import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class BetaGoblin(MetaGoblin):

    '''
    for scen7 variants
    mode options:
        - iter: for multiple links (using external links file)
    accepts:
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
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        self.mode = mode

    def extract_id(self, url):
        return re.search(r'[a-z0-9]+_([a-z0-9]+)*', url).group()

    def correct_format(self, url):
        if re.search(r'[a-z0-9]+_([a-z0-9]+)*', url):
            return True
        else:
            return False

    def run(self):
        if 'scene7' in self.url:
            links = [self.url]
        else:
            links = {l.group() for l in re.finditer(r'\w+\.scene7[^" \n]+', self.get_html(self.url))}
        for link in links:
            if not self.correct_format(link):
                continue
            base, query = self.identify(link)
            id = self.extract_id(link)
            for char in self.chars:
                self.loot(f'{base}{id}{char}{query}')
                sleep(self.tickrate)
