import re

from goblins.meta import MetaGoblin


class SavageXGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https?://[^" \n]+\d-800x800\.jpg'

    def __str__(self):
        return 'savagex goblin'

    def __repr__(self):
        return 'savagex'

    def strip(self, url):
        '''strip end of url and return the base'''
        return re.sub(r'(LAYDOWN|\d)\-\d+x\d+\.jpg', '', url)

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'cdn.savagex' in target:
                urls = [target]
            else:
                urls = self.extract_urls_greedy(self.url_pat, target)
            for url in urls:
                for n in range(1, 5):
                    self.collect(self.strip(url) + f'{n}-1600x1600.jpg')
        self.loot()
        self.cleanup(self.path_main)
