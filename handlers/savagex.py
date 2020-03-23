import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class SavageXGoblin(MetaGoblin):

    '''
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'savagex goblin'

    def strip(self, url):
        return re.sub(r'(LAYDOWN|\d)\-\d+x\d+.jpg', '', url)

    def run(self):
        if 'cdn.savagex' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(r'https*://[^" \n]+\d\-800x800.jpg', self.args['url'])
        for link in links:
            for n in range(1, 5):
                self.loot(self.strip(link) + f'{n}-1600x1600.jpg')
                sleep(self.args['tickrate'])
        self.cleanup(self.path_main)
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
