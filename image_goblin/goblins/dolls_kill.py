import re

from goblins.meta import MetaGoblin


class DollsKillGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'dolls kill goblin'
    ID = 'dollskill'
    URL_PAT = r'img src="https?://media\.dollskill\.com[^" \']+\-\d+\.jpe?g'

    def __init__(self, args):
        super().__init__(args)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'media.dollskill' in target:
                urls = [target]
                self.logger.log(1, self.NAME, 'WARNING', 'image urls not fully supported')
            else:
                urls = self.extract_by_regex(self.URL_PAT, target)
            for url in urls:
                self.collect(re.sub(r'\d+\.jpg', '1.jpeg', url).replace('img src="', ''))
        self.loot()
