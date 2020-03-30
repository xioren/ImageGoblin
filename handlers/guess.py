import re
from handlers.meta_goblin import MetaGoblin


class GuessGoblin(MetaGoblin):

    '''
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'guess goblin'

    def run(self):
        if 'guess-img' in self.args['url']:
            links = [self.args['url']]
        else:
            links = []
            if not self.args['silent']:
                print(f'[{self.__str__()}] <WARNING> url type not supported')
            # links = self.extract_links(r'https://res\.cloudinary\.com/guess\-img/[^" ]+\?pgw=1', self.args['url'])
        for link in links:
            base = re.sub(r'c_fill[^/]+/c_fill[^/]+/', '', re.sub(r'-ALT\d', '', self.dequery(link)))
            for id in ('', '-ALT1', '-ALT2', '-ALT3', '-ALT4'):
                self.collect(f'{base}{id}')
        self.loot()
