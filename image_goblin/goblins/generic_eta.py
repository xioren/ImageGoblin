import re

from goblins.meta import MetaGoblin


class EtaGoblin(MetaGoblin):
    '''handles: adis.ws
    accepts:
        - image
        - webpage
    generic back-end for:
        - ann summers
        - boohoo
        - nasty gal
    '''

    def __init__(self, args):
        super().__init__(args)
        self.query = '?scl=1&qlt=100'
        self.url_pat = r'i\d\.adis\.ws/i/[a-z]+/[\w_]+'
        self.modifiers = [f'_{n}' for n in range(1, 10)]
        self.modifiers.insert(0, '')

    def __str__(self):
        return 'eta goblin'

    def __repr__(self):
        return 'eta'

    def trim(self, url):
        '''trim the url down'''
        return re.search(self.url_pat, url).group().rstrip("_s/").replace('media.nastygal.com',
                                                                          'i1.adis.ws')

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if '/i/' in target:
                urls = [target]
            else:
                urls = self.extract_by_regex(self.url_pat, target)
            for url in urls:
                for mod in self.modifiers:
                    self.collect(f'{self.trim(url)}{mod}.jpg{self.query}')
        self.loot()
