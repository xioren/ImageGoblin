import re

from goblins.meta import MetaGoblin


class DollsKillGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'img src="https?://media\.dollskill\.com[^" \']+\-\d+\.jpe?g'

    def __str__(self):
        return 'dolls kill goblin'

    def __repr__(self):
        return 'dollskill'

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'media.dollskill' in target:
                urls = [target]
                self.logger.log(1, self.__str__(), 'WARNING', 'image urls not fully supported')
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                self.collect(re.sub(r'\d+\.jpg', '1.jpeg', url).replace('img src="', ''))
        self.loot()
