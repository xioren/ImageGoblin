import re

from goblins.meta import MetaGoblin


# NOTE: can scale with c_scale,h_5058,q_100


class CAGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'c&a goblin'
    ID = 'canda'
    URL_PAT = r'https?://www\.c-and-a\.com/productimages/[^"\s]+/v[^"\s]+-0[1-9]\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        '''extract image id from url'''
        return re.search(r'/\d+-\d+', url).group()

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'productimages' in target:
                urls = [target]
            else:
                urls = self.extract_by_regex(self.URL_PAT, target)
            for url in urls:
                id = self.extract_id(url)
                for n in range(1, 6):
                    self.collect(f'https://www.c-and-a.com/productimages/q_100{id}-0{n}.jpg')
        self.loot()
