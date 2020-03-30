import re
from handlers.meta_goblin import MetaGoblin

# NOTE: may work for trendyol

class EpsilonGoblin(MetaGoblin):

    '''
    handles: Medianova CDN
    docs: https://docs.medianova.com/image-resize-and-optimization-module/
    accepts:
        - image
        - webpage
    generic back-end for:
        - koton
        - yargici
    '''

    def __init__(self, args):
        super().__init__(args)

    def clean(self, url):
        return re.sub(r'mnresize/\d+/\d+', '', self.custom(url))

    def run(self):
        if 'mncdn' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(self.img_pat, self.args['url'])
        for link in links:
            base, _ = re.split(self.mod_pat, self.clean(link))
            self.generate_modifiers(link)
            for mod in self.modifiers:
                self.collect(f'{base}{mod}{self.end}')
        self.loot()
