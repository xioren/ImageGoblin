import re

from goblins.meta import MetaGoblin

# BUG: does not work ---> different (new) url formats to consider

class ElcorteGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https?://sgfm\.elcorteingles[^" ]+\d+x\d+\.jpg'

    def __str__(self):
        return 'elcorte goblin'

    def __repr__(self):
        return 'elcorteingles'

    def extract_id(self, url):
        '''extract image id from url'''
        return re.search(r'\d+_', url).group().strip('_')

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'sgfm.elcorteingles' in target:
                urls = [target]
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                id = self.extract_id(url)
                iter = int(id)
                for n in range(iter - 5, iter + 6):
                    self.collect(f'https://sgfm.elcorteingles.es/SGFM/dctm/MARKET/{id[:3]}/{id[3:6]}/{id[6:9]}/{n}_WWW_967x1200.jpg')
        self.loot()
