import re

from goblins.meta import MetaGoblin


class TallyWeijlGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'tally weijl goblin'
    ID = 'tallyweijl'
    URL_PAT = r'https?://www\.tally\-weijl\.com/img/[^"\s]+\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        urls = []

        for target in self.args['targets'][self.ID]:
            if '/img/' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                url.append(target)
            else:
                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

        for url in urls:
            self.collect(re.sub(r'img/\d+/\d+', 'img/1800/1800', url))

        self.loot()
