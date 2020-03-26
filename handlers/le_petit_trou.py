import re
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
            self.collect(re.sub(r'th\d+', 'orig', link))
        self.loot()
