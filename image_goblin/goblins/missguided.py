import re

from goblins.meta import MetaGoblin


class MissguidedGoblin(MetaGoblin):
    '''accepts:
        - image
    '''

    NAME = 'missguided goblin'
    ID = 'missguided'
    URL_BASE = 'https://media.missguided.com/i/missguided/'
    # URL_PAT = r'https?://media\.missguided\.com[^"\s]+_\d{2}\.jpg'
    QUERY = '?fmt=jpeg&qlty=100'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        '''extract image id from url'''
        return re.search(r'[A-Z\d]+', url).group().upper()

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'media.missguided' in target:
                urls.append(target)
            else:
                # BUG: currently throws 405 error. requires cookie uuid values. unknown how they are generated.
                self.logger.log(2, self.NAME, 'WARNING', 'webpage urls not supported', once=True)

        for url in urls:
            id = self.extract_id(url)

            for n in range(1, 6):
                if self.args['mode'] == 'png':
                    self.collect(f'{self.URL_BASE}{id}_0{n}?fmt=png')
                else:
                    self.collect(f'{self.URL_BASE}{id}_0{n}{self.QUERY}')

        self.loot()
        self.cleanup(self.path_main)
