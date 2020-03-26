import re
from handlers.meta_goblin import MetaGoblin


class MaisonLejabyGoblin(MetaGoblin):

    '''
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'maison lejaby goblin'

    def run(self):
        if '.jpg' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(r'https://www\.maisonlejaby\.com.+\.jpg', self.args['url'])
        for link in links:
            link = re.sub(r'[A-Z]\.jpg', '', link).replace('medium', 'large')
            for char in ('A', 'B', 'C', 'D', 'E', 'F'):
                self.collect(f'{link}{char}.jpg')
        self.loot()
