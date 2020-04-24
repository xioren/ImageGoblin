import re

from goblins.meta import MetaGoblin

# sometimes throws 502 errors

class ZetaGoblin(MetaGoblin):
    '''handles: Calzedonia Group
    accepts:
        - image
        - webpage
    generic back-end for:
        - intimissimi
        - tezenis
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https?://images\.calzedonia\.com/get/w/\d+/\w+_wear_\w+\.jpg'
        self.modifiers = ('FI', 'BI', 'M', 'DT1', 'C', 'B', 'F')

    def __str__(self):
        return 'zeta goblin'

    def __repr__(self):
        return 'zeta'

    def trim(self, url):
        '''remove cropping, end of url and return base'''
        return re.sub(r'w/\d+', 'w/3400', re.sub(r'[A-Z0-9]+\.jpg|h/\d+/', '', url))

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'calzedonia' in target:
                urls = [target]
            else:
                urls = self.extract_by_regex(self.url_pat, target)
            for url in urls:
                base = self.trim(url)
                for mod in self.modifiers:
                    self.collect(f'{base}{mod}.jpg')
        self.loot()
