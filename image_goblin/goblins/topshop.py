from parsing import *
from goblins.meta import MetaGoblin


class TopshopGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'images\.topshop\.com/i/TopShop/[A-Z\d]+_[A-Z]_\d\.jpg'

    def __str__(self):
        return 'topshop goblin'

    def __repr__(self):
        return 'topshop'

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'images.topshop' in target:
                urls = [target]
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                for n in range(1, 6):
                    self.collect('{}{}.jpg'.format(self.dequery(url)[:-5], n))
        self.loot()
