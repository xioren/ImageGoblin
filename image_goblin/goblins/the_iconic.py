import re

from goblins.meta import MetaGoblin


class TheIconicGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'the iconic goblin'
    ID = 'theiconic'
    URL_PAT = r'(\d+-){2}\d\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        '''extract image id from url'''
        return re.search(r'\d+-\d+-', url).group()

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'img1' in target or 'static' in target:
                urls = [target]
            else:
                urls = self.extract_by_regex(self.URL_PAT, target)
            for url in urls:
                id = self.extract_id(url)
                for n in range(1, 6):
                    self.collect(f'https://static.theiconic.com.au/p/{id}{n}.jpg')
        self.loot()
