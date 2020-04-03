import re
from handlers.meta_goblin import MetaGoblin


class ZetaGoblin(MetaGoblin):

    '''
    handles: Calzedonia Group
    accepts:
        - image
        - webpage
    generic back-end for:
        - intimissimi
        - tezenis
    '''

    def __init__(self, args):
        super().__init__(args)
        self.link_pat = r'https://images\.calzedonia\.com/get/w/\d+/\w+_wear_\w+\.jpg'
        self.modifiers = ('FI', 'BI', 'M', 'DT1', 'C', 'B', 'F')

    def __str__(self):
        return 'zeta goblin'

    def prep(self, url):
        return re.sub(r'h/\d+/', '', re.sub(r'w/\d+', 'w/3400', re.sub(r'[A-Z0-9]+\.jpg', '', url)))

    def run(self):
        if 'calzedonia' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(self.link_pat, self.args['url'])
        for link in links:
            base = self.prep(link)
            for mod in self.modifiers:
                self.collect(f'{base}{mod}.jpg')
        self.loot()
