import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class BoohooGoblin(MetaGoblin):

    '''
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'boohoo goblin'

    def extract_id(self, url):
        return re.search(r'\w+_\w+_xl', url).group()

    def run(self):
        id = self.extract_id(self.args['url'])
        self.loot(f'https://i1.adis.ws/i/boohooamplience/{id}')
        sleep(self.args['tickrate'])
        for n in range(1, 6):
            self.loot(f'https://i1.adis.ws/i/boohooamplience/{id}_{n}')
            sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
