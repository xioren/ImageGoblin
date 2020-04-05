import re
from goblins.meta_goblin import MetaGoblin


class MissguidedGoblin(MetaGoblin):

    '''
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'missguided goblin'

    def __repr__(self):
        return 'missguided'

    def extract_id(self, url):
        return re.search(r'[A-Z\d]+', url).group().upper()

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'media.missguided' in target:
                urls = [target]
            else:
                # NOTE: currently throws 405 error
                # urls = self.extract_urls(r'https://media\.missguided\.com[^" ]+_\d{2}\.jpg', target)
                urls = []
                if not self.args['silent']:
                    print(f'[{self.__str__()}] <WARNING> url type not supported')
            for url in urls:
                id = self.extract_id(self.args['url'])
                for n in range(1, 6):
                    self.collect(f'https://media.missguided.com/i/missguided/{id}_0{n}')
        self.loot()
        if not self.args['nodl'] and not self.args['noclean']:
            self.cleanup(self.path_main)
