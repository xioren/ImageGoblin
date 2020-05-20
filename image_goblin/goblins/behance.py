import re
import json

from goblins.meta import MetaGoblin


class BehanceGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'behance goblin'
    ID = 'behance'

    def __init__(self, args):
        super().__init__(args)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'mir-s3-cdn' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(re.sub(r'(?<=modules/)[^/]+', 'source', target))
            else:
                self.headers.update({'X-Requested-With': 'XMLHttpRequest',
                                     'Cookie': 'ilo0=true'})

                response = json.loads(self.get(target).content)

                for module in response['view']['project']['modules']:
                    if module.get('sizes'):
                        urls.append(module['sizes']['original'])

        for url in urls:
            self.collect(url)

        self.loot()
