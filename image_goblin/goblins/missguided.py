import re

from goblins.meta import MetaGoblin


class MissguidedGoblin(MetaGoblin):
    '''accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https?://media\.missguided\.com[^" ]+_\d{2}\.jpg'

    def __str__(self):
        return 'missguided goblin'

    def __repr__(self):
        return 'missguided'

    def extract_id(self, url):
        '''extract image id from url'''
        return re.search(r'[A-Z\d]+', url).group().upper()

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'media.missguided' in target:
                urls = [target]
            else:
                # NOTE: currently throws 405 error. apparently very strict bot/vpn prevention.
                urls = []
                self.logger.log(1, self.__str__(), 'WARNING', 'webpage urls not supported')
            for url in urls:
                id = self.extract_id(url)
                for n in range(1, 6):
                    self.collect(f'https://media.missguided.com/i/missguided/{id}_0{n}')
        self.loot()
        self.cleanup(self.path_main)
