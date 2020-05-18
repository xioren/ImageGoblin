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

    NAME = 'eta goblin'
    ID = 'eta'
    QUERY = '?scl=1&qlt=100'
    URL_PAT = r'i\d\.adis\.ws/i/[a-z]+/[\w_]+'
    MODIFIERS = [f'_{n}' for n in range(1, 10)]

    def __init__(self, args):
        super().__init__(args)
        self.MODIFIERS.insert(0, '')

    def __str__(self):
        return 'eta goblin'

    def __repr__(self):
        return 'eta'

    def trim(self, url):
        '''trim the url down'''
        return re.search(self.URL_PAT, url).group().rstrip("_s/").replace('media.nastygal.com', 'i1.adis.ws')

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')

        for target in self.args['targets'][self.ID]:
            if '/i/' in target:
                urls = [target]
            else:
                urls = self.parser.extract_by_regex(self.get(target).content, self.URL_PAT)

            for url in urls:
                for mod in self.MODIFIERS:
                    self.collect(f'{self.trim(url)}{mod}.jpg{self.QUERY}')

        self.loot()
