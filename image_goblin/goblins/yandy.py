import re

from goblins.meta import MetaGoblin


class YandyGoblin(MetaGoblin):
    '''accepts:
        - image*
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
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'assets.yandycdn' in target:
                urls = [target]
                self.logger.log(1, self.__str__(), 'WARNING', 'image urls not fully supported')
            else:
                urls = self.extract_by_regex(self.url_pat, target)
            for url in urls:
                self.collect(url.replace('Products', 'HiRez'))
        self.loot()
