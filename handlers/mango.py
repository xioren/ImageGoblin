import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class MangoGoblin(MetaGoblin):

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
        return 'mango goblin'

    def extract(self, url):
        url = re.sub('/outfit|-9+_01', '', url)
        return re.sub(r'S\d+', 'S20', re.search(r'[\w/:\.]+_\w+', url).group())

    def run(self):
        base = self.extract(self.url)
        self.loot(re.sub('fotos', 'fotos/outfit', base) + '-99999999_01.jpg')
        sleep(self.tickrate)
        for id in ('', '_R', '_D1', '_D2', '_D3', '_D4', '_D5', '_D6'):
            self.loot(f'{base}{id}.jpg')
            sleep(self.tickrate)
