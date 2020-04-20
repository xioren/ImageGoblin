import re

from goblins.meta import MetaGoblin


class GuessGoblin(MetaGoblin):
    '''accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https?://res\.cloudinary\.com/guess-img/[^" ]+\?pgw=1'

    def __str__(self):
        return 'guess goblin'

    def __repr__(self):
        return 'guess'

    def trim(self, url):
        '''decrop and return url base'''
        return re.sub(r'(?<=/)([a-z]{,2}_\w+(,|/)?)+/v\d+/|-ALT\d', '', self.parser.dequery(url))

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'guess-img' in target:
                urls = [target]
            else:
                urls = []
                self.logger.log(1, self.__str__(), 'WARNING', 'webpage urls not supported')
            for url in urls:
                url_base = self.trim(url)
                for id in ('', '-ALT1', '-ALT2', '-ALT3', '-ALT4'):
                    self.collect(f'{url_base}{id}')
        self.loot()
