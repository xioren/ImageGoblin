import re
import json

from goblins.meta import MetaGoblin


class MangoGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'mango goblin'
    ID = 'mango'
    # URL_PAT = r'https?://st\.mngbcn\.com[^"\?\s]+\.jpg'
    QUERY = '?qlt=100'
    MODIFIERS = ('', '_R', '_D1', '_D2', '_D3', '_D4', '_D5', '_D6')
    IMAGE_URL = 'https://st.mngbcn.com/rcs/pics/static'
    API_URL = 'https://shop.mango.com/services/garments'
    STOCK_ID_URL = 'https://shop.mango.com/services/stock-id'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        '''extract image id and T number from url'''
        return re.search(r'T\d', url).group(), re.search(r'\d+_\d+', url).group()

    def extract_product(self, url):
        '''extract product id from url'''
        return re.search(r'(?<=_)\d+(?=\.)', url).group()

    def run(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'mngbcn' in target:
                t, id = self.extract_id(target)

                urls.append(f'{self.IMAGE_URL}/{t}/fotos/outfit/S20/{id}-99999999_01.jpg')
                for mod in self.MODIFIERS:
                    urls.append(f'{self.IMAGE_URL}/{t}/fotos/S20/{id}{mod}.jpg')
            else:
                init_response = self.get(target, store_cookies=True)
                self.set_cookies()

                stock_id = json.loads(self.get(self.STOCK_ID_URL).content)['key']
                self.headers.update({'stock-id': stock_id})

                response = json.loads(self.get(f'{self.API_URL}/{self.extract_product(target)}').content)

                for color in response['colors']['colors']:
                    for images in color['images']:
                        for image in images:
                            urls.append(f'{self.IMAGE_URL}{image["url"]}')

        for url in urls:
            self.collect(f'{self.parser.dequery(url)}{self.QUERY}')

        self.loot()
