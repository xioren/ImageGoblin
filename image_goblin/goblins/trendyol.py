import re
from goblins.meta_goblin import MetaGoblin

# NOTE: may have switched to new cdn; investigate.
# legacy: https://www.trendyol.com/assets/product/media/images/20191021/17/449253/57309150/5/5_org_zoom.jpg

class TrendyolGoblin(MetaGoblin):

    '''
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https://img-trendyol\.mncdn\.com/Assets/ProductImages/\w+/\w+/[^" ,]+\.jpg'

    def __str__(self):
        return 'trandyol goblin'

    def __repr__(self):
        return 'trandyol'

    def extract_base(self, url):
        return re.sub(r'\d+_[a-z]+(_[a-z]+)*\.jpg', '', url)

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'img-trendyol' in target:
                urls = [target]
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                base = self.extract_base(url)
                for n in range(1, 16):
                    self.collect(f'{base}{n}_org_zoom.jpg')
        self.loot()
