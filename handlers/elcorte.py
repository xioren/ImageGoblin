import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class ElcorteGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    link types:
        - image
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        self.mode = mode
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'elcorte goblin'

    def prep(self, url):
        return re.sub(r'\d+_+\d+x\d+.jpg', '', url)

    def extract_id(self, link):
        return re.search(r'_+\d+_+', link).group().strip('_')

    def run(self):
        id = self.extract_id(self.url)
        for n in range(6):
            if len(id) == 1:
                # NOTE: this might be unecessary as their format may have changed perm.
                self.loot(self.prep(id) + f'{n}__967x1200.jpg')
            else:
                self.loot(self.prep(id) + f'0{n}_967x1200.jpg')
            sleep(self.tickrate)
