import re

from goblins.meta import MetaGoblin


class SavageXGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'savagex goblin'
    ID = 'savagex'
    URL_PAT = r'https?://[^" \n]+\d-800x800\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def strip(self, url):
        '''strip end of url and return the base'''
        return re.sub(r'(LAYDOWN|\d)\-\d+x\d+\.jpg', '', url)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'cdn.savagex' in target:
                urls = [target]
            else:
                urls = self.extract_by_regex(self.URL_PAT, target)
            for url in urls:
                for n in range(1, 5):
                    self.collect(self.strip(url) + f'{n}-1600x1600.jpg')
        self.loot()
        self.cleanup(self.path_main)
