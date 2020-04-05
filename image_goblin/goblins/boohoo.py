import re
from goblins.meta import MetaGoblin


class BoohooGoblin(MetaGoblin):

    '''
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'i\d\.adis\.ws/i/boohooamplience/[^" \?]+'
        self.url_base = 'https://i1.adis.ws/i/boohooamplience/'
        self.modifiers = ('', '_1', '_2', '_3', '_4')

    def __str__(self):
        return 'boohoo goblin'

    def __repr__(self):
        return 'boohoo'

    def extract_id(self, url):
        return re.search(r'[a-z\d]+_[a-z\d]+_xl', url).group()

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'adis.ws' in target:
                urls = [target]
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                id = self.extract_id(url)
                for mod in self.modifiers:
                    self.collect(f'{self.url_base}{id}{n}')
        self.loot()
