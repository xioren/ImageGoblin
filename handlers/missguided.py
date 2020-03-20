import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class MissguidedGoblin(MetaGoblin):

    '''
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'missguided goblin'

    def extract(self, url):
        return re.search(r'[A-Z\d]+', url).group().upper()

    def run(self):
        id = self.extract(self.args['url'])
        for n in range(1, 6):
            self.loot(f'https://media.missguided.com/i/missguided/{id}_0{n}')
            sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
