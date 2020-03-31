import re
from handlers.meta_goblin import MetaGoblin


class NastyGalGoblin(MetaGoblin):

    '''
    mode options:
        -
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.link_pat = r'media\.nastygal\.com/i/nastygal/[^" \?]+'

    def __str__(self):
        return 'nasty gal goblin'

    def extract_id(self, url):
        return re.search(r'[a-z\d]+_[a-z\d]+_xl', url).group()

    def run(self):
        if 'adis.ws' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(self.link_pat, self.args['url'])
        for link in links:
            id = self.extract_id(link)
            for n in ('', '_1', '_2', '_3', '_4'):
                self.collect(f'https://i1.adis.ws/i/boohooamplience/{id}{n}')
        self.loot()
