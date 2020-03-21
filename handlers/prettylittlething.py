import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class PrettyLittleThingGoblin(MetaGoblin):

    '''
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'prettylittlething goblin'

    def run(self):
        for link in self.extract_links(r'https://cdn\-img\.prettylittlething\.com[^" \n]+', self.args['url']):
            self.loot(link, clean=True)
            sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
