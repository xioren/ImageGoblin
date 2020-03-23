from time import sleep
from parsing import *
from handlers.meta_goblin import MetaGoblin


class TopshopGoblin(MetaGoblin):

    '''
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'topshop goblin'

    def run(self):
        if 'images.topshop' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(r'images\.topshop\.com/i/TopShop/[A-Z\d]+_[A-Z]_\d\.jpg', self.args['url'])
        for link in links:
            for n in range(1, 6):
                self.loot('{}{}.jpg'.format(self.dequery(link)[:-5], n))
                sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
