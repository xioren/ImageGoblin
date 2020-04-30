import re

from goblins.meta import MetaGoblin


class MaisonLejabyGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'maison lejaby goblin'
    ID = 'maisonlejaby'
    URL_PAT = r'maisonlejaby\.com/phototheque/[^" ]+\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'phototheque' in target:
                urls = [target]
            else:
                urls = self.extract_by_regex(self.URL_PAT, target)
            for url in urls:
                url_base = re.sub(r'[A-Z](\.[A-Z0-9]+)?\.jpg', '', url).replace('medium', 'large')
                for mod in ('A', 'B', 'C', 'D', 'E', 'F'):
                    self.collect(f'{url_base}{mod}.jpg')
        self.loot()
