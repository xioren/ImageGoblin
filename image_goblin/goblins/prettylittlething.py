import re

from goblins.meta import MetaGoblin


class PrettyLittleThingGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'prettylittlething goblin'
    ID = 'prettylittlething'
    URL_PAT = r'https?://cdn-img\.prettylittlething\.com[^"\s\n]+'

    def __init__(self, args):
        super().__init__(args)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'cdn-img.prettylittlething' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(target)
            else:
                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

        for url in urls:
            self.collect(url, clean=True)

        self.loot()
