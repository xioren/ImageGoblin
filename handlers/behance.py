import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class BehanceGoblin(MetaGoblin):

    '''
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)
        self.img_pat = r'https://mir-s3-cdn-cf.behance.net/project_modules/[\w/\.]+\.[A-Za-z]+'
        self.size_pat = r'1400(_opt_1)*|max_1200|disp'
        self.sizes = ('max_3840', 'fs', '1400', 'max_1200', 'disp')

    def __str__(self):
        return 'behance goblin'

    def fit(self, url, size):
        return re.sub(self.size_pat, size, self.args['url'])

    def run(self):
        for size in self.sizes:
            attempt = self.loot(self.fit(self.args['url'], size))
            if attempt:
                break
            sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
