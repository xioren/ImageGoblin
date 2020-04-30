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

    def trim_url(self, url):
        '''remove cropping from url'''
        return re.sub(r'mnresize/\d+/\d+', '', url).replace('Thumbs', 'Originals')

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'mncdn' in target:
                urls = [target]
            else:
                urls = self.extract_by_regex(self.URL_PAT, target)
            for url in urls:
                url_base, _ = re.split(self.MOD_PAT, self.trim_url(url))
                self.generate_modifiers(url)
                for mod in self.modifiers:
                    self.collect(f'{url_base}{mod}{self.URL_END}')
        self.loot()
