import re
from goblins.meta import MetaGoblin


# NOTE: can scale with c_scale,h_5058,q_100


class CAGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https://www\.c-and-a\.com/productimages/[^" ]+/v[^" ]+-0[1-9]\.jpg'

    def __str__(self):
        return 'c&a goblin'

    def __repr__(self):
        return 'canda'

    def extract_id(self, url):
        '''extract image id from url'''
        return re.search(r'/\d+-\d+', url).group()

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'productimages' in target:
                urls = [target]
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                id = self.extract_id(url)
                for n in range(1, 6):
                    self.collect(f'https://www.c-and-a.com/productimages/q_100{id}-0{n}.jpg')
        self.loot()
