import re
from handlers.meta_goblin import MetaGoblin


class EpsilonGoblin(MetaGoblin):

    '''
    handles: Medianova CDN
    docs: https://docs.medianova.com/image-resize-and-optimization-module/
    accepts:
        - image
        - webpage
    generic back-end for:
        - koton
    '''

    def __init__(self, args):
        super().__init__(args)

    def clean(self, url):
        return re.sub(r'mnresize/\d+/\d+', '', url)

    def run(self):
        if 'mncdn' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(self.img_pat, self.args['url'])
        for link in links:
            base, end = re.split(self.id_pat, self.clean(link))
            for id in self.ids:
                self.collect(f'{base}{id}{end}')
        self.loot()
