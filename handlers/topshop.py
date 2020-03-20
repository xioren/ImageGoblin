from time import sleep
from parsing import *
from handlers.meta_goblin import MetaGoblin


class TopshopGoblin(MetaGoblin):

    '''
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'topshop goblin'

    def run(self):
        link = self.dequery(self.args['url'])[:-5]
        for n in range(1, 6):
            self.loot(f'{url}{n}.jpg')
            sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
