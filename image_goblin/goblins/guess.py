import re
from goblins.meta_goblin import MetaGoblin


class GuessGoblin(MetaGoblin):

    '''
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'guess goblin'

    def __repr__(self):
        return 'guess'

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'guess-img' in target:
                urls = [target]
            else:
                urls = []
                if not self.args['silent']:
                    print(f'[{self.__str__()}] <WARNING> url type not supported')
                # urls = self.extract_urls(r'https://res\.cloudinary\.com/guess\-img/[^" ]+\?pgw=1', self.args['url'])
            for url in urls:
                base = re.sub(r'c_fill[^/]+/c_fill[^/]+/', '', re.sub(r'-ALT\d', '', self.dequery(url)))
                for id in ('', '-ALT1', '-ALT2', '-ALT3', '-ALT4'):
                    self.collect(f'{base}{id}')
        self.loot()
