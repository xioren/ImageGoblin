import json

from re import sub

from goblins.meta import MetaGoblin


class SavageXGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'savagex goblin'
    ID = 'savagex'
    # URL_PAT = r'https?://[^"\s\n]+\d-800x800\.jpg'
    API_URL = 'https://www.savagex.com/api'
    API_AUTH_URL = API_URL + '/sessions'

    def __init__(self, args):
        super().__init__(args)

    def product_id(self, url):
        '''extract product id from url'''
        return self.parser.dequery(url).split('-')[-1]

    def run(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'cdn.savagex' in target:
                urls.append(target)
            else:
                init_response = self.get(target, store_cookies=True)
                self.set_cookies()
                # QUESTION: does this change? can storedomain be extracted from req url?
                self.headers.update({'x-api-key': 'V0X9UnXkvO4vTk1gYHnpz7jQyAMO64Qp4ONV2ygu',
                                     'x-tfg-storedomain':'www.savagex.com'})

                auth = self.get(self.API_AUTH_URL, store_cookies=True)
                self.set_cookies()

                response = json.loads(self.get(f'{self.API_URL}/products/{self.product_id(target)}').content)
                urls.extend(response['image_view_list'])

        self.delay()

        for url in urls:
            if 'laydown' in url or 'LAYDOWN' in url: # skip product images
                continue

            self.collect(sub(r'\d+x\d+', '1600x1600', url))

        self.loot()
