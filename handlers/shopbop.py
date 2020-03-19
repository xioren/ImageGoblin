import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class ShopbopGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    link types:
        - image
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, tickrate, verbose, nodl)
        self.mode = mode
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'shopbop goblin'

    def run(self):
        link = re.sub(r'._\w+(_\w+)*_\w+_', '', self.url).replace('m.media', 'images-na.ssl-images').repalce('2-1', '2-0')
        for n in range(1, 7):
            self.loot(re.sub(r'q\d', fr'q{n}', self.url))
            sleep(self.tickrate)
