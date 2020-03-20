import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class MangoGoblin(MetaGoblin):

    '''
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'mango goblin'

    def extract(self, url):
        url = re.sub('/outfit|-9+_01', '', url)
        return re.sub(r'S\d+', 'S20', re.search(r'[\w/:\.]+_\w+', url).group())

    def run(self):
        base = self.extract(self.args['url'])
        self.loot(re.sub('fotos', 'fotos/outfit', base) + '-99999999_01.jpg')
        sleep(self.args['tickrate'])
        for id in ('', '_R', '_D1', '_D2', '_D3', '_D4', '_D5', '_D6'):
            self.loot(f'{base}{id}.jpg')
            sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
