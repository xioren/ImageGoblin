import re
from handlers.meta_goblin import MetaGoblin


class Goblin(MetaGoblin):

    '''
    accepts:
        -
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return ' goblin'

    def run(self):
        if '' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(r'', self.args['url'])
        for link in links:
            self.collect(link)
        self.loot()
