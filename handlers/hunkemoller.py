import re
from time import sleep
from handlers.meta_goblin import MetaGoblin

# NOTE: can also use generic gamma, but might be lesser resolution

class HunkemollerGoblin(MetaGoblin):

    '''
    accepts:
        - image
        - web page
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'hunkemoller goblin'

    def run(self):
        id = re.search(r'(/|-)\d+', self.args['url']).group().replace('/', '').replace('-', '')
        for num in range(1, 6):
            self.loot(f'https://images-hunkemoller.akamaized.net/original/{id}_{num}.jpg')
            sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
