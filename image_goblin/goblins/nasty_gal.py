import re

from goblins.meta import MetaGoblin

# TODO: shares cdn with booho...combine?

class NastyGalGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'media\.nastygal\.com/i/nastygal/[^" \?]+'

    def __str__(self):
        return 'nasty gal goblin'

    def __repr__(self):
        return 'nastygal'

    def extract_id(self, url):
        '''extract image id from url'''
        return re.search(r'[a-z\d]+_[a-z\d]+_xl', url).group()

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'media.nastygal' in target:
                urls = [target]
            else:
                urls = self.extract_urls_greedy(self.url_pat, target)
            for url in urls:
                id = self.extract_id(url)
                for n in ('', '_1', '_2', '_3', '_4'):
                    self.collect(f'https://i1.adis.ws/i/boohooamplience/{id}{n}')
        self.loot()
