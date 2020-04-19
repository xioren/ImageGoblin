import re

from goblins.meta import MetaGoblin


class LePetitTrouGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https?://cdn\.shoplo[^"]+\.jpg'

    def __str__(self):
        return 'le-petit-trou goblin'

    def __repr__(self):
        return 'lepetittrou'

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'shoplo' in target:
                urls = [target]
                self.logger.log(1, self.__str__(), 'WARNING', 'image urls not fully supported')
            else:
                urls = self.extract_urls_greedy(self.url_pat, target)
            for url in urls:
                self.collect(re.sub(r'th\d+', 'orig', url))
        self.loot()
