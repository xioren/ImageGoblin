import re
from goblins.meta import MetaGoblin


class MaisonLejabyGoblin(MetaGoblin):

    '''
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https://www\.maisonlejaby\.com.+\.jpg'

    def __str__(self):
        return 'maison lejaby goblin'

    def __repr__(self):
        return 'maisonlejaby'

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if '.jpg' in target:
                urls = [target]
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                url = re.sub(r'[A-Z]\.jpg', '', url).replace('medium', 'large')
                for char in ('A', 'B', 'C', 'D', 'E', 'F'):
                    self.collect(f'{url}{char}.jpg')
        self.loot()
