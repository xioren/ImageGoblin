import re
from handlers.meta_goblin import MetaGoblin


class MissguidedGoblin(MetaGoblin):

    '''
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'missguided goblin'

    def extract_id(self, url):
        return re.search(r'[A-Z\d]+', url).group().upper()

    def run(self):
        if 'media.missguided' in self.args['url']:
            links = [self.args['url']]
        else:
            # NOTE: currently throws 405 error
            # links = self.extract_links(r'https://media\.missguided\.com[^" ]+_\d{2}\.jpg', self.args['url'])
            links = []
            if not self.args['silent']:
                print(f'[{self.__str__()}] <WARNING> url type not supported')
        for link in links:
            id = self.extract_id(self.args['url'])
            for n in range(1, 6):
                self.collect(f'https://media.missguided.com/i/missguided/{id}_0{n}')
        self.loot()
