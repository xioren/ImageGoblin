import re
from handlers.meta_goblin import MetaGoblin

# removing /dw/image/v2/AAYL_PRD give original image, while leaving it in allow resizing
# TODO: handle both image and webpage urls

class GammaGoblin(MetaGoblin):

    '''
    for on.demandware variants
    accepts:
        - image
        - webpage
    generic backend for:
        - boux avenue
        - etam
        - hunkemoller
        - sandro
        - springfield
        - womens secret
    '''

    def __init__(self, args):
        super().__init__(args)

    def extract(self, url):
        iter = re.search(self.iter, url).group()
        id, end = url.split(iter)
        return id, iter, end

    def isolate(self, url):
        return re.search(r'/*[^/]+\.jpe*g', url).group().lstrip('/')

    def run(self):
        if 'demandware' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(fr'[^" ]+demandware[^" ]+{self.pattern}', self.args['url'])
        for link in links:
            id, iter, end = self.extract(self.isolate(link))
            # self.generate_modifiers(iter)
            for mod in self.modifiers:
                self.collect(f'{self.base}{id}{mod}{end}')
        self.loot()
