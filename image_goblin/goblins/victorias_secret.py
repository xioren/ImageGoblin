import re
from goblins.meta_goblin import MetaGoblin


class VictoriasSecretGoblin(MetaGoblin):

    '''
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'victorias secret goblin'

    def __repr__(self):
        return 'victoriassecret'

    def extract(self, url):
        return re.search(r'\w+.jpg', url).group()

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'victoriassecret.com/p/' in target:
                # NOTE: does not scan
                urls = [target]
            else:
                # urls = self.extract_urls(r'https*://www\.victoriassecret\.com/p/[^" ]+\.jpg', self.args['url'])
                urls = []
                if not self.args['silent']:
                    print(f'[{self.__str__()}] <WARNING> url type not supported')
            for url in urls:
                self.collect(re.sub(r'p/\d+x\d+', 'p/4040x5390', target))
        self.loot()
