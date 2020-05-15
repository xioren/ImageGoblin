import re

from goblins.meta import MetaGoblin


class BehanceGoblin(MetaGoblin):
    '''accepts:
        - image*
    '''

    NAME = 'behance goblin'
    ID = 'behance'
    # URL_PAT = r'https?://mir-s3-cdn-cf\.behance\.net/project_modules/[\w/\.]+\.[A-Za-z]+'
    SIZE_PAT = r'1400(_opt_1)*|max_1200|disp'
    SIZES = ('max_3840', 'fs', '1400', 'max_1200', 'disp')

    def __init__(self, args):
        super().__init__(args)

    def fit(self, url, size):
        '''sub size into url'''
        return re.sub(self.SIZE_PAT, size, url)

    def run(self):
        self.logger.log(1, self.NAME, 'scanning sizes')
        self.toggle_collecton_type()
        for target in self.args['targets'][self.ID]:
            if 'mir-s3-cdn' in target:
                urls = [target]
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
            else:
                urls = []
                self.logger.log(2, self.NAME, 'WARNING', 'webpage urls not supported', once=True)
            for url in urls:
                for size in self.SIZES:
                    new_url = self.fit(url, size)
                    if self.get(new_url).code == 200:
                        self.collect(new_url)
                        break
            self.loot()
