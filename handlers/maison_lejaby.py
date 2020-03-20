import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class MaisonLejabyGoblin(MetaGoblin):

    '''
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'maison lejaby goblin'

    def run(self):
        if '.html' in self.args['url']:
            links = {l.group() for l in re.finditer(r'https://www\.maisonlejaby\.com.+\.jpg', self.get_html(self.args['url']))}
        else:
            links = [self.args['url']]
        for link in links:
            link = re.sub(r'[A-Z]\.jpg', '', link).replace('medium', 'large')
            for char in ('A', 'B', 'C', 'D', 'E', 'F'):
                self.loot(f'{link}{char}.jpg')
                sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
