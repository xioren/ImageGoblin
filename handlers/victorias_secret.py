import re
from handlers.meta_goblin import MetaGoblin


class VictoriasSecretGoblin(MetaGoblin):

    '''
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'victorias secret goblin'

    def extract(self, link):
        return re.search(r'\w+.jpg', link).group()

    def run(self):
        if 'victoriassecret.com/p/' in self.args['url']:
            # NOTE: does not scan
            links = [self.args['url']]
        else:
            # links = self.extract_links(r'https*://www\.victoriassecret\.com/p/[^" ]+\.jpg', self.args['url'])
            links = []
            if not self.args['silent']:
                print(f'[{self.__str__()}] <WARNING> url type not supported')
        for link in links:
            self.collect(re.sub(r'\d+x\d+', '4040x5390', self.args['url']))
        self.loot()
