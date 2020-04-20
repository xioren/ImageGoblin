import re
import json

from goblins.meta import MetaGoblin


class ImgurGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage*
    '''

    def __init__(self, args):
        super().__init__(args)
        # self.url_pat = r''

    def __str__(self):
        return 'imgur goblin'

    def __repr__(self):
        return 'imgur'

    def prep(self, url):
        '''upgrade image size'''
        if len(self.parser.extract_filename(url)) == 8:
            url = url.replace('b.', '.')
        return url.replace('m.imgur', 'i.imgur')

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'i.imgur' in target or 'm.imgur' in target:
                urls = [target]
            else:
                urls = []
                if 'gallery' in target:
                    self.logger.log(1, self.__str__(), 'WARNING', 'https://imgur.com/gallery/XXXXXXX urls not supported')
                else:
                    matches = self.extract_arbitrary(target, r'(?<=image               : ){[^\n]+}(?=,\n)')
                    for match in matches:
                        items = x = json.loads(match.group())
                        for item in items['album_images']['images']:
                            urls.append(f'https://i.imgur.com/{item["hash"]}{item["ext"]}')
            for url in urls:
                self.collect(self.prep(url))
        self.loot()
