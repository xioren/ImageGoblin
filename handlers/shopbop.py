import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class ShopbopGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'shopbop goblin'

    def run(self):
        link = re.sub(r'._\w+(_\w+)*_\w+_', '', self.args['url']).replace('m.media', 'images-na.ssl-images').repalce('2-1', '2-0')
        for n in range(1, 7):
            self.loot(re.sub(r'q\d', fr'q{n}', self.args['url']))
            sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
