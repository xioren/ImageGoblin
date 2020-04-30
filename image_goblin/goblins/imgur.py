import re
import json

from goblins.meta import MetaGoblin


class ImgurGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage*
    '''

    NAME = 'imgur goblin'
    ID = 'imgur'

    def __init__(self, args):
        super().__init__(args)

    def prep(self, url):
        '''upgrade image size'''
        if len(self.parser.extract_filename(url)) == 8:
            url = url.replace('b.', '.')
        return url.replace('m.imgur', 'i.imgur')

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'i.imgur' in target or 'm.imgur' in target:
                urls = [target]
            else:
                urls = []
                if 'gallery' in target:
                    self.logger.log(1, self.NAME, 'WARNING', 'https://imgur.com/gallery/XXXXXXX urls not supported')
                else:
                    matches = self.extract_by_regex(r'(?<=image\s+:\s){[^\n]+}(?=,\n)', target)
                    for match in matches:
                        items = json.loads(match)
                        for item in items['album_images']['images']:
                            urls.append(f'https://i.imgur.com/{item["hash"]}{item["ext"]}')
            for url in urls:
                self.collect(self.prep(url))
        self.loot()
