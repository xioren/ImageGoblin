import re

from goblins.meta import MetaGoblin


class Goblin(MetaGoblin):
    '''accepts:
        -
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r''

    def __str__(self):
        return ' goblin'

    def __repr__(self):
        return ''

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if '' in target:
                urls = [target]
            else:
                urls = self.extract_urls_greedy(target)
            for url in urls:
                self.collect(url)
        self.loot()
