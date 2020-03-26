import re
from handlers.meta_goblin import MetaGoblin


class TrendyolGoblin(MetaGoblin):

    '''
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'trandyol goblin'

    def extract_base(self, url):
        return re.sub(r'\d+_[a-z]+(_[a-z]+)*\.jpg', '', url)

    def run(self):
        if 'img-trendyol' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(r'https://img-trendyol\.mncdn\.com/Assets/ProductImages/\w+/\w+/[^" ,]+\.jpg', self.args['url'])
        for link in links:
            base = self.extract_base(link)
            for n in range(1, 16):
                self.collect(f'{base}{n}_org_zoom.jpg')
        self.loot()
