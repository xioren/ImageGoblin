import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class LePetitTrouGoblin(MetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'le-petit-trou goblin'

    def run(self):
        if 'shoplo' in self.args['url']:
            links = [self.args['url']]
        else:
            links = {l.group() for l in re.finditer(r'https://cdn.shoplo[^"]+\.jpg', self.get_html(self.args['url']))}
        for link in links:
            self.loot(re.sub(r'th\d+', 'orig', link))
            sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
