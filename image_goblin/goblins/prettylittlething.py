import re
from goblins.meta import MetaGoblin


class PrettyLittleThingGoblin(MetaGoblin):
    '''accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https://cdn\-img\.prettylittlething\.com[^" \n]+'

    def __str__(self):
        return 'prettylittlething goblin'

    def __repr__(self):
        return 'prettylittlething'

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'cdn-img.prettylittlething' in target:
                urls = []
                if not self.args['silent']:
                    print(f'[{self.__str__()}] <WARNING> url type not supported')
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                self.collect(url, clean=True)
        self.loot()
