import json

from urllib.parse import quote_plus

from goblins.meta import MetaGoblin


class TopshopGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'topshop goblin'
    ID = 'topshop'
    # URL_PAT = r'images\.topshop\.com/i/TopShop/[A-Z\d]+_[A-Z]_\d\.jpg'
    QUERY = '?scl=1&qlt=100'
    API_URL = 'https://www.topshop.com/api/products/'

    def __init__(self, args):
        super().__init__(args)

    def extract_info(self, url):
        '''extract product path and brand code from url'''
        path = url.replace('https://', '').split('/')[1:]
        brand_code = path[1]
        return '/'.join(path), brand_code

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'images.topshop' in target:
                for n in range(1, 6):
                    urls.append(f'{self.parser.dequery(target)[:-5]}{n}.jpg')
            else:
                path, brand_code = self.extract_info(target)
                self.headers.update({'BRAND-CODE': brand_code})

                response = json.loads(self.get(f'{self.API_URL}{quote_plus(f"/{path}")}').content)

                for asset in response['assets']:
                    if asset['assetType'] == 'IMAGE_LARGE':
                        urls.append(asset['url'])

        for url in urls:
            self.collect(f'{self.parser.dequery(url)}{self.QUERY}')

        self.loot()
