import re
from handlers.meta_goblin import MetaGoblin

# TODO: finds lots of duplicates...improve.

class ShopbopGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'shopbop goblin'

    def run(self):
        if 'amazon' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(r'https://[a-z\-\.]+amazon\.com[^" ]+\.jpg', self.args['url'])
        for link in links:
            link = re.sub(r'._\w+(_\w+)*_\w+_', '', link).replace('m.media', 'images-na.ssl-images').replace('2-1', '2-0')
            for n in range(1, 7):
                self.collect(re.sub(r'q\d', fr'q{n}', link))
        self.loot()
