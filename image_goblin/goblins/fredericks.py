import re

from goblins.meta import MetaGoblin


class FredericksGoblin(MetaGoblin):
    '''accepts:
        - image*
    '''

    NAME = 'fredericks goblin'
    ID = 'fredericks'
    # URL_PAT = r'//[^"\s\n]+\.jpe?g'

    def __init__(self, args):
        super().__init__(args)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'cloudfront' in target:
                urls = [target]
                self.logger.log(2, self.__str__(), 'WARNING', 'image urls not fully supported', once=True)
            else:
                urls = []
                self.logger.log(2, self.__str__(), 'WARNING', 'webpage urls not supported', once=True)
            for url in urls:
                self.collect(re.sub(r'\.\d+w', '', url))
        self.loot()
