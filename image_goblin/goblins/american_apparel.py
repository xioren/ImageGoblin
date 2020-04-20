import re

from goblins.meta import MetaGoblin

# TODO: add bigcommerce cdn generic goblin

class AmericanApparelGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https?://cdn\d+\.bigcommerce\.com/[^/]+/images/stencil/[^/]+' \
                       r'/products/\d+/\d+/[a-z0-9]+_[a-z0-9]+_[^" ]+\.jpg'

    def __str__(self):
        return 'american apparel goblin'

    def __repr__(self):
        return 'americanapparel'

    def split_url(self, url):
        '''split url into base, end and sub out cropping'''
        return re.split(r'_(\d{2})?(?=_)', re.sub(r'(?<=stencil/)[^/]+', 'original', url), 1)

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'bigcommerce' in target:
                urls = [self.parser.dequery(target)]
            else:
                urls = self.extract_urls_greedy(self.url_pat, target)
            for url in urls:
                url_base, _, url_end = self.split_url(url)
                for mod in ('', '01', '02', '03', '04'):
                    self.collect(f'{url_base}_{mod}{url_end}')
        self.loot()
