import re

from goblins.meta import MetaGoblin


class TallyWeijlGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'tally weijl goblin'
    ID = 'tallyweijl'
    URL_PAT = r'https?://www\.tally\-weijl\.com/img/[^" ]+\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if '/img/' in target:
                urls = [target]
                self.logger.log(1, self.NAME, 'WARNING', 'image urls not fully supported')
            else:
                urls = self.extract_by_regex(self.URL_PAT, target)
            for url in urls:
                self.collect(re.sub(r'img/\d+/\d+', 'img/1800/1800', url))
        self.loot()
