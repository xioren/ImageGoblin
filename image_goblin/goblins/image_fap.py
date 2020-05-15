import re

from goblins.meta import MetaGoblin


class ImageFapGoblin(MetaGoblin):
    '''accepts:
        - webpage
    '''

    NAME = 'image fap goblin'
    ID = 'imagefap'
    URL_PAT = re.compile(r'https?://cdn\.imagefap\.com/images/full/[^"\s<]+')

    def __init__(self, args):
        super().__init__(args)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'cdn.imagefap' in target:
                urls = [target]
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not supported', once=True)
            else:
                urls = []
                links = self.extract_by_tag(f'{self.parser.dequery(target)}?view=2', 'a', 'href')
                for link in links:
                    if '/photo/' in link:
                        urls.extend(self.extract_by_regex(self.URL_PAT, f'https://www.imagefap.com{link}'))
            for url in urls:
                self.collect(url)
        self.loot()
