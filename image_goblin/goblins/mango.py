import re

from goblins.meta import MetaGoblin


class MangoGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'mango goblin'
    ID = 'mango'
    URL_PAT = r'https?://st\.mngbcn\.com[^"\?\s]+\.jpg'
    QUERY = '?qlt=100'
    MODIFIERS = ('', '_R', '_D1', '_D2', '_D3', '_D4', '_D5', '_D6')
    URL_BASE = 'https://st.mngbcn.com/rcs/pics/static/'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        '''extract image id from url'''
        return re.search(r'T\d', url).group(), re.search(r'\d+_\d+', url).group()

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'mngbcn' in target:
                urls = [target]
            else:
                urls = self.extract_by_regex(self.URL_PAT, target)
            for url in urls:
                t, id = self.extract_id(url)
                self.collect(f'{self.URL_BASE}{t}/fotos/outfit/S20/{id}-99999999_01.jpg{self.QUERY}')
                for mod in self.MODIFIERS:
                    self.collect(f'{self.URL_BASE}{t}/fotos/S20/{id}{mod}.jpg{self.QUERY}')
        self.loot()
