import re
from goblins.meta_goblin import MetaGoblin


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
        self.url_pat = r'i\d\.adis\.ws/i/annsummers/\d+_Z'

    def __str__(self):
        return 'ann summers goblin'

    def __repr__(self):
        return 'annsummers'

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'adis.ws' in target:
                urls = [target]
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                url = re.sub(r'(_\d)?\.jpg', '', self.dequery(url))
                for mod in self.modifiers:
                    self.collect(f'{url}{mod}.jpg{self.query}')
        self.loot()
