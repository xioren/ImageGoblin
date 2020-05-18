import re

from goblins.meta import MetaGoblin


class BurberryGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'burberry goblin'
    ID = 'burberry'
    URL_PAT = r'https?://assets\.burberry\.com/is/image/Burberryltd/[^"\s]+'

    def __init__(self, args):
        super().__init__(args)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')

        for target in self.args['targets'][self.ID]:
            if 'assets.burberry' in target:
                urls = [target]
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
            else:
                urls = self.parser.extract_by_regex(self.get(target).content, self.URL_PAT)

            for url in urls:
                self.collect(f'{self.parser.dequery(url)}?scl=1')

        self.loot()
