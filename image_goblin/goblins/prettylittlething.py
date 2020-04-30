import re

from goblins.meta import MetaGoblin


class PrettyLittleThingGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'prettylittlething goblin'
    ID = 'prettylittlething'
    URL_PAT = r'https?://cdn-img\.prettylittlething\.com[^" \n]+'

    def __init__(self, args):
        super().__init__(args)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'cdn-img.prettylittlething' in target:
                urls = [target]
                self.logger.log(1, self.NAME, 'WARNING', 'image urls not fully supported')
            else:
                urls = self.extract_by_regex(self.URL_PAT, target)
            for url in urls:
                self.collect(url, clean=True)
        self.loot()
