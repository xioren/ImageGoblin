import re
import json

from goblins.meta import MetaGoblin


# NOTE:  _OM_ -> model image | _OF_ -> product image
# TEMP: 4040x5390


class VictoriasSecretGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'victorias secret goblin'
    ID = 'victoriassecret'
    URL_BASE = 'https://www.victoriassecret.com'
    API_URL_BASE = 'https://api.victoriassecret.com'

    def __init__(self, args):
        super().__init__(args)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []
        if self.args['noup']:
            dimensions = 'p/760x1013'
        else:
            dimensions = 'p/3040x4052'

        for target in self.args['targets'][self.ID]:
            if '/p/' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(re.sub(r'p/\d+x\d+', dimensions, target.replace('dm.', 'www.')))
            else:
                # NOTE: version is there too if needed; might always be V6.
                for path in self.parser.extract_by_regex(self.get(target).content, r'(?<="path":")page/[^"]+'):
                    response = json.loads(self.get(f'{self.API_URL_BASE}/products/v6/{path}').content)
                    for product in response['product']['purchasableImages']:
                        for choice in product['choices']:
                            for image in choice['images']:
                                urls.append(f'{self.URL_BASE}/p/{dimensions}/{image["image"]}.jpg')

        for url in urls:
            if '_OF_' in url: # skip product images
                continue

            self.collect(url)

        self.loot()
