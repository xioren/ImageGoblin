import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class LePetitTrouGoblin(MetaGoblin):

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'le-petit-trou goblin'

    def run(self):
        if 'shoplo' in self.url:
            links = [self.url]
        else:
            links = {l.group() for l in re.finditer(r'https://cdn.shoplo[^"]+\.jpg', self.get_html(self.url))}
        for link in links:
            self.loot(re.sub(r'th\d+', 'orig', link))
            sleep(self.tickrate)
