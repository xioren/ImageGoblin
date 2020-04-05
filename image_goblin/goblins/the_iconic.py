import re
from goblins.meta import MetaGoblin


class TheIconicGoblin(MetaGoblin):

    '''
    mode options:
        -
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'(\d+\-){2}\d\.jpg'

    def __str__(self):
        return 'the iconic goblin'

    def __repr__(self):
        return 'theiconic'

    def extract_id(self, url):
        return re.search(r'\d+\-\d+\-', url).group()

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'img1' in target or 'static' in target:
                urls = [target]
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                id = self.extract_id(url)
                for n in range(1, 6):
                    self.collect(f'https://static.theiconic.com.au/p/{id}{n}.jpg')
        self.loot()
