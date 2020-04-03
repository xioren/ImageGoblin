import re
from handlers.meta_goblin import MetaGoblin


# NOTE: can scale with c_scale,h_5058,q_100


class CAGoblin(MetaGoblin):

    '''
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.link_pat = r'https://www\.c-and-a\.com/productimages/[^" ]+/v[^" ]+-0[1-9]\.jpg'

    def __str__(self):
        return 'c&a goblin'

    def extract_id(self, url):
        return re.search(r'/\d+-\d+', url).group()

    def run(self):
        if 'productimages' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(self.link_pat, self.args['url'])
        for link in links:
            id = self.extract_id(link)
            for n in range(1, 6):
                self.collect(f'https://www.c-and-a.com/productimages/q_100{id}-0{n}.jpg')
        self.loot()
