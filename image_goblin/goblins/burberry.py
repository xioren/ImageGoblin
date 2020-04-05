import re
from goblins.meta_goblin import MetaGoblin


class BurberryGoblin(MetaGoblin):

    '''
    accepts:
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https*://assets.burberry[^"]+\.jpe*g'

    def __str__(self):
        return 'burberry goblin'

    def __repr__(self):
        return 'burberry'

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'assets.burberry' in target:
                urls = []
                if not self.args['silent']:
                    print(f'[{self.__str__()}] <WARNING> url type not supported')
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                self.collect(f'{url}?scl=1')
        self.loot()
