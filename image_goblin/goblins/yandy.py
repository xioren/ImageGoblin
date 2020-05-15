import re

from goblins.meta import MetaGoblin


class YandyGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'yandy goblin'
    ID = 'yandy'
    URL_PAT = r'https?://assets\.yandycdn\.com/Products/[^-]+-\d+\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'assets.yandycdn' in target:
                urls = [target]
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
            else:
                urls = self.extract_by_regex(self.URL_PAT, target)
            for url in urls:
                self.collect(url.replace('Products', 'HiRez'))
        self.loot()
