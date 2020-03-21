import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class YandyGoblin(MetaGoblin):

    '''
    accepts:
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'yandy goblin'

    def run(self):
        for link in self.extract_links(r'https://assets.yandycdn.com/Products/[^-]+-\d+.jpg', self.args['url']):
            self.loot(link.replace('Products', 'HiRez'))
            sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
