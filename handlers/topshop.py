from parsing import *
from handlers.meta_goblin import MetaGoblin


class TopshopGoblin(MetaGoblin):

    '''
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.link_pat = r'images\.topshop\.com/i/TopShop/[A-Z\d]+_[A-Z]_\d\.jpg'

    def __str__(self):
        return 'topshop goblin'

    def run(self):
        if 'images.topshop' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(self.link_pat, self.args['url'])
        for link in links:
            for n in range(1, 6):
                self.collect('{}{}.jpg'.format(self.dequery(link)[:-5], n))
        self.loot()
