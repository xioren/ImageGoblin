import re

from goblins.meta import MetaGoblin

# NOTE: may work for trendyol

class EpsilonGoblin(MetaGoblin):
    '''handles: Medianova CDN
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

    def prep(self, url):
        '''remove cropping'''
        return re.sub(r'mnresize/\d+/\d+', '', url).replace('Thumbs', 'Originals')

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'mncdn' in target:
                urls = [target]
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                url_base, _ = re.split(self.mod_pat, self.prep(url))
                self.generate_modifiers(url)
                for mod in self.modifiers:
                    self.collect(f'{url_base}{mod}{self.url_end}')
        self.loot()
