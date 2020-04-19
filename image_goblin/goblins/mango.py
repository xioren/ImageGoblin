import re

from goblins.meta import MetaGoblin


class MangoGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https?://st\.mngbcn\.com[^"\? ]+\.jpg'
        self.query = '?qlt=100'
        self.modifiers = ('', '_R', '_D1', '_D2', '_D3', '_D4', '_D5', '_D6')

    def __str__(self):
        return 'mango goblin'

    def __repr__(self):
        return 'mango'

    def extract_id(self, url):
        '''extract image id from url'''
        return re.search(r'T\d', url).group(), re.search(r'\d+_\d+', url).group()

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'mngbcn' in target:
                urls = [target]
            else:
                urls = self.extract_urls_greedy(self.url_pat, target)
            for url in urls:
                t, id = self.extract_id(url)
                self.collect(f'https://st.mngbcn.com/rcs/pics/static/{t}/fotos/outfit/S20/{id}-99999999_01.jpg{self.query}')
                for mod in self.modifiers:
                    self.collect(f'https://st.mngbcn.com/rcs/pics/static/{t}/fotos/S20/{id}{mod}.jpg{self.query}')
        self.loot()
