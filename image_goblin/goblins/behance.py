import json

from re import sub

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
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'mir-s3-cdn' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(sub(r'(?<=modules/)[^/]+', 'source', target))
            else:
                self.headers.update({'X-Requested-With': 'XMLHttpRequest',
                                     'Cookie': 'ilo0=true'})

                response = json.loads(self.get(target).content)

                if 'view' in response:
                    for module in response['view']['project']['modules']:
                        if 'sizes' in module:
                            urls.append(module['sizes']['original'])

            self.delay()

        for url in urls:
            self.collect(url)

        self.loot()
