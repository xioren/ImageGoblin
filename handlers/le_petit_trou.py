import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class LePetitTrouGoblin(MetaGoblin):
    '''
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'le-petit-trou goblin'

    def run(self):
        if 'shoplo' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(r'https://cdn.shoplo[^"]+\.jpg', self.args['url'])
        for link in links:
            self.loot(re.sub(r'th\d+', 'orig', link))
            sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
