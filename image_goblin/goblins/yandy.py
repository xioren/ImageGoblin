import re

from goblins.meta import MetaGoblin

# QUESTION: can this handle single image?

class YandyGoblin(MetaGoblin):
    '''accepts:
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https://assets.yandycdn.com/Products/[^-]+-\d+.jpg'

    def __str__(self):
        return 'yandy goblin'

    def __repr__(self):
        return 'yandy'

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'assets.yandycdn' in target:
                urls = []
                if not self.args['silent']:
                    print(f'[{self.__str__()}] <WARNING> image urls not supported')
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                self.collect(url.replace('Products', 'HiRez'))
        self.loot()
