import re

from goblins.meta import MetaGoblin

# NOTE: may have switched to new cdn; investigate.
# legacy: https://www.trendyol.com/assets/product/media/images/20191021/17/449253/57309150/5/5_org_zoom.jpg

class TrendyolGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'trandyol goblin'
    ID = 'trendyol'
    URL_PAT = r'https?://(img-trendyol\.mncdn|cdn\.dsmcdn)\.com/[^"\s,]+\d_org(_zoom)?\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def extract_base(self, url):
        '''extract base of url'''
        return re.sub(r'\d+_[a-z]+(_[a-z]+)?\.jpg', '', url)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')

        for target in self.args['targets'][self.ID]:
            if 'img-trendyol' in target or 'cdn.dsmcdn' in target:
                urls = [target]
            else:
                urls = self.parser.extract_by_regex(self.get(target).content, self.URL_PAT)

            for url in urls:
                url_base = self.extract_base(url)

                for n in range(1, 16):
                    self.collect(f'{url_base}{n}_org_zoom.jpg')

        self.loot()
