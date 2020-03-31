import re
from handlers.meta_goblin import MetaGoblin

# BUG: does not work ---> different (new) url formats to consider

class ElcorteGoblin(MetaGoblin):

    '''
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.link_pat = r'https://sgfm.elcorteingles[^" ]+\.jpg'

    def __str__(self):
        return 'elcorte goblin'

    def remove_end(self, url):
        return re.sub(r'\d+_+\d+x\d+.jpg', '', url)

    def extract_id(self, link):
        return re.search(r'([A-Za-z\d]+_){2}', link).group().strip('_')

    def run(self):
        if 'sgfm.elcorteingles' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(self.link_pat, self.args['url'])
        for link in links:
            id = self.extract_id(self.args['url'])
            for n in range(6):
                if len(id) == 1:
                    # NOTE: this might be unecessary as their format may have changed perm.
                    self.collect(self.remove_end(id) + f'{n}__967x1200.jpg')
                else:
                    self.collect(self.remove_end(id) + f'0{n}_967x1200.jpg')
        self.loot()
