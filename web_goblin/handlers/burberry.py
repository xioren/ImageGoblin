import re
from handlers.meta_goblin import MetaGoblin


class BurberryGoblin(MetaGoblin):

    '''
    accepts:
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.link_pat = r'https*://assets.burberry[^"]+\.jpe*g'

    def __str__(self):
        return 'burberry goblin'

    def run(self):
        if 'assets.burberry' in self.args['url']:
            links = []
            if not self.args['silent']:
                print(f'[{self.__str__()}] <WARNING> url type not supported')
        else:
            links = self.extract_links(self.link_pat, self.args['url'])
        for link in link:
            self.collect(f'{link}?wid=3072&hei=3072')
        self.loot()
