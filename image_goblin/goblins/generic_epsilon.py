import re
from goblins.meta_goblin import MetaGoblin

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
        for target in self.args['targets'][self.__repr__()]:
            if 'mncdn' in target:
                urls = [target]
            else:
                urls = self.extract_urls(self.url_pat, self.args['url'])
            for url in urls:
                base, _ = re.split(self.mod_pat, self.clean(url))
                self.generate_modifiers(url)
                for mod in self.modifiers:
                    self.collect(f'{base}{mod}{self.end}')
        self.loot()
