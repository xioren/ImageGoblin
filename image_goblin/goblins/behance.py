import re

from goblins.meta import MetaGoblin

# TODO: needs better approach

class BehanceGoblin(MetaGoblin):
    '''accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https?://mir-s3-cdn-cf\.behance\.net/project_modules/[\w/\.]+\.[A-Za-z]+'
        self.size_pat = r'1400(_opt_1)*|max_1200|disp'
        self.sizes = ('max_3840', 'fs', '1400', 'max_1200', 'disp')

    def __str__(self):
        return 'behance goblin'

    def __repr__(self):
        return 'behance'

    def fit(self, url, size):
        '''sub size into url'''
        return re.sub(self.size_pat, size, url)

    def run(self):
        self.toggle_collecton_type()
        for target in self.args['targets'][self.__repr__()]:
            if 'mir-s3-cdn' in target:
                # NOTE: does not scan
                urls = [target]
            else:
                urls = []
                if not self.args['silent']:
                    print(f'[{self.__str__()}] <WARNING> webpage urls not supported')
            for url in urls:
                for size in self.sizes:
                    self.collect(self.fit(url, size))
        self.loot()
