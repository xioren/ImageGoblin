import re
import json

from goblins.meta import MetaGoblin


# NOTE: sign in gate bypass -> /embed?pub=true


class ImgurGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage*
    '''

    NAME = 'imgur goblin'
    ID = 'imgur'
    BASE_URL = 'https://i.imgur.com/'

    def __init__(self, args):
        super().__init__(args)


    def clean(self, url):
        return re.sub(r'#.+$', '', self.parser.dequery(url))

    def prep(self, url):
        '''upgrade image size'''
        filename  = self.parser.extract_filename(url)
        if len(filename) == 8:
            url = f'{self.BASE_URL}{filename[:-1]}.jpg'
        return url.replace('m.imgur', 'i.imgur')

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'i.imgur' in target or 'm.imgur' in target:
                urls = [target]
            else:
                urls = []
                matches = self.extract_by_regex(r'(?<=image               :\s){[^\n]+}(?=,\n)', self.clean(target))
                for match in matches:
                    items = json.loads(match)
                    for item in items['album_images']['images']:
                        urls.append(f'{self.BASE_URL}{item["hash"]}{item["ext"]}')
                if not urls: # sign in probably required -> try bypass
                    matches = self.extract_by_regex(r'(?<=images            =\s){[^\n]+}(?=,\n)',
                                                    f'{self.clean(target)}/embed?pub=true')
                    for match in matches:
                        items = json.loads(match)
                        for item in items['images']:
                            urls.append(f'{self.BASE_URL}{item["hash"]}{item["ext"]}')
            for url in urls:
                self.collect(self.prep(url))
        self.loot()
