import re

from goblins.meta import MetaGoblin


class TallyWeijlGoblin(MetaGoblin):
    '''accepts:
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https?://www\.tally\-weijl\.com/img/[^" ]+\.jpg'

    def __str__(self):
        return 'tally weijl goblin'

    def __repr__(self):
        return 'tallyweijl'

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if '/img/' in target:
                urls = []
                self.logger.log(1, self.__str__(), 'WARNING', 'image urls not supported')
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                self.collect(re.sub(r'img/\d+/\d+', 'img/1800/1800', url))
        self.loot()
