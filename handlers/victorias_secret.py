import re
from time import sleep
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
        # TODO: add link dragnet
        self.loot(re.sub(r'\d+x\d+', '4040x5390', self.args['url']))
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
