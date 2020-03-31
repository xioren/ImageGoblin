import re
from handlers.meta_goblin import MetaGoblin


# NOTE: some images use demandware


class AnnSummersGoblin(MetaGoblin):

    '''
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.query = '?scl=1&qlt=100'
        self.modifiers = ('', '_1', '_2', '_3', '_4')
        self.link_pat = r'i\d\.adis\.ws/i/annsummers/\d+_Z'

    def __str__(self):
        return 'ann summers goblin'

    def run(self):
        if 'adis.ws' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(self.link_pat, self.args['url'])
        for link in links:
            link = re.sub(r'(_\d)?\.jpg', '', self.dequery(link))
            for mod in self.modifiers:
                self.collect(f'{link}{mod}.jpg{self.query}')
        self.loot()
