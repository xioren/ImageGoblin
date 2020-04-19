import re

from goblins.meta import MetaGoblin


class MaisonLejabyGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'maisonlejaby\.com/phototheque/[^" ]+\.jpg'

    def __str__(self):
        return 'maison lejaby goblin'

    def __repr__(self):
        return 'maisonlejaby'

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'phototheque' in target:
                urls = [target]
            else:
                urls = self.extract_urls_greedy(self.url_pat, target)
            for url in urls:
                url_base = re.sub(r'[A-Z](\.[A-Z0-9]+)?\.jpg', '', url).replace('medium', 'large')
                for mod in ('A', 'B', 'C', 'D', 'E', 'F'):
                    self.collect(f'{url_base}{mod}.jpg')
        self.loot()
