import re

from goblins.meta import MetaGoblin


class GuessGoblin(MetaGoblin):
    '''accepts:
        - image
    '''

    NAME = 'guess goblin'
    ID = 'guess'
    # URL_PAT = r'https?://res\.cloudinary\.com/guess-img/[^" ]+\?pgw=1'

    def __init__(self, args):
        super().__init__(args)

    def trim(self, url):
        '''decrop and return url base'''
        return re.sub(r'(?<=/)([a-z]{,2}_\w+(,|/)?)+/v\d+/|-ALT\d', '', self.parser.dequery(url))

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'guess-img' in target:
                urls = [target]
            else:
                urls = []
                self.logger.log(2, self.NAME, 'WARNING', 'webpage urls not supported', once=True)
            for url in urls:
                url_base = self.trim(url)
                for id in ('', '-ALT1', '-ALT2', '-ALT3', '-ALT4'):
                    self.collect(f'{url_base}{id}')
        self.loot()
