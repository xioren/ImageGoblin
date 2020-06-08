import re

from goblins.meta import MetaGoblin


class LePetitTrouGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'le-petit-trou goblin'
    ID = 'lepetittrou'
    URL_PAT = r'https?://cdn\.shoplo[^"]+\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'shoplo' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(target)
            else:
                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            self.collect(re.sub(r'th\d+', 'orig', url))

        self.loot()
