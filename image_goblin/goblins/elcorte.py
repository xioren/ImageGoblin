import re
from goblins.meta import MetaGoblin

# BUG: does not work ---> different (new) url formats to consider

class ElcorteGoblin(MetaGoblin):

    '''
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https://sgfm.elcorteingles[^" ]+\.jpg'

    def __str__(self):
        return 'elcorte goblin'

    def __repr__(self):
        return 'elcorteingles'

    def remove_end(self, url):
        return re.sub(r'\d+_+\d+x\d+.jpg', '', url)

    def extract_id(self, url):
        return re.search(r'([A-Za-z\d]+_){2}', url).group().strip('_')

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'sgfm.elcorteingles' in target:
                urls = [target]
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                # QUESTION: extract from target or each url?
                id = self.extract_id(url)
                for n in range(6):
                    if len(id) == 1:
                        # NOTE: this might be unecessary as their format may have changed perm.
                        self.collect(self.remove_end(id) + f'{n}__967x1200.jpg')
                    else:
                        self.collect(self.remove_end(id) + f'0{n}_967x1200.jpg')
        self.loot()
