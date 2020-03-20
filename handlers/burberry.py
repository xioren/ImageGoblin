import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class BurberryGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    link types:
        - webpage
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'burberry goblin'

    def run(self):
        links = {l.group() for l in re.finditer(r'https*://assets.burberry[^"]+\.jpe*g', self.get_html(self.url))}
        for link in links:
            self.loot(f'{link}?wid=3072&hei=3072')
            sleep(self.tickrate)
