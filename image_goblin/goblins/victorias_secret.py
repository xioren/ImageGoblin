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
    URL_BASE = 'https://www.victoriassecret.com/'
    API_URL_BASE = 'https://api.victoriassecret.com/'

    def __init__(self, args):
        super().__init__(args)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'victoriassecret.com/p/' in target:
                urls = [target]
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
            else:
                urls = []
                # NOTE: version is there too if needed; might always be V6.
                for path in self.extract_by_regex(r'(?<="path":")page/[^"]+', target):
                    response = json.loads(self.get(f'{self.API_URL_BASE}products/v6/{path}').content)
                    for product in response['product']['purchasableImages']:
                        for choice in product['choices']:
                            for image in choice['images']:
                                urls.append(f'{self.URL_BASE}p/3040x4052/{image["image"]}.jpg')
            for url in urls:
                if '_OF_' in url: # skip product images
                    continue
                if self.args['noup']:
                    self.collect(re.sub(r'p/\d+x\d+', 'p/760x1013', url))
                else:
                    self.collect(re.sub(r'p/\d+x\d+', 'p/3040x4052', url))
        self.loot()
