import re

from goblins.meta import MetaGoblin


class GuessGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'guess goblin'
    ID = 'guess'
    URL_PAT = r'https?://res\.cloudinary\.com/guess-img/image/upload/f_auto[^"\s\']+/Style/[^"\s\']+'

    def __init__(self, args):
        super().__init__(args)

    def trim(self, url):
        '''decrop and return url base'''
        return re.sub(r'(?<=upload/).+/v1/|-ALT\d', '', self.parser.dequery(url))

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')

        for target in self.args['targets'][self.ID]:
            if 'guess-img' in target:
                urls = [target]
            else:
                urls = self.parser.extract_by_regex(self.get(target).content, self.URL_PAT)

            for url in urls:
                url_base = self.trim(url)

                for id in ('', '-ALT1', '-ALT2', '-ALT3', '-ALT4'):
                    self.collect(f'{url_base}{id}')

        self.loot()
