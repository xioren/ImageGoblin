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

    URL_PAT = r'https?://images\.calzedonia\.com/get/w/\d+/\w+_wear_\w+\.jpg'
    MODIFIERS = ('FI', 'BI', 'M', 'DT1', 'C', 'B', 'F')

    def __init__(self, args):
        super().__init__(args)

    def trim(self, url):
        '''remove cropping, end of url and return base'''
        return re.sub(r'w/\d+', 'w/3400', re.sub(r'[A-Z0-9]+\.jpg|h/\d+/', '', url))

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'calzedonia' in target:
                urls = [target]
            else:
                urls = self.extract_by_regex(self.URL_PAT, target)
            for url in urls:
                base = self.trim(url)
                for mod in self.MODIFIERS:
                    self.collect(f'{base}{mod}.jpg')
        self.loot()
