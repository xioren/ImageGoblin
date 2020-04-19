import re

from goblins.meta import MetaGoblin


class FredericksGoblin(MetaGoblin):
    '''accepts:
        - image*
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'//[^" \n]+\.jpe?g'

    def __str__(self):
        return 'fredericks goblin'

    def __repr__(self):
        return 'fredericks'

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'cloudfront' in target:
                urls = [target]
                self.logger.log(1, self.__str__(), 'WARNING', 'image urls not fully supported')
            else:
                urls = []
                self.logger.log(1, self.__str__(), 'WARNING', 'webpage urls not supported')
            for url in urls:
                self.collect(re.sub(r'\.\d+w', '', url))
        self.loot()
