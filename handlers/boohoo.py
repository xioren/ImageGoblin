import re
from handlers.meta_goblin import MetaGoblin


class BoohooGoblin(MetaGoblin):

    '''
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.link_pat = r'i\d\.adis\.ws/i/boohooamplience/[^" \?]+'
        self.link_base = 'https://i1.adis.ws/i/boohooamplience/'
        self.modifiers = ('', '_1', '_2', '_3', '_4')

    def __str__(self):
        return 'boohoo goblin'

    def extract_id(self, url):
        return re.search(r'[a-z\d]+_[a-z\d]+_xl', url).group()

    def run(self):
        if 'adis.ws' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(self.link_pat, self.args['url'])
        for link in links:
            id = self.extract_id(link)
            for mod in self.modifiers:
                self.collect(f'{self.link_base}{id}{n}')
        self.loot()
