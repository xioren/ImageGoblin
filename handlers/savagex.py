import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class SavageXGoblin(MetaGoblin):

    '''
    accepts:
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.image_pat = r'https*://[^" \n]+800x800.jpg'

    def __str__(self):
        return 'savagex goblin'

    def run(self):
        for link in self.extract_links(self.image_pat, self.args['url']):
            self.loot(link.replace('800x800', '1600x1600'))
            sleep(self.args['tickrate'])
        self.cleanup(self.path_main)
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
