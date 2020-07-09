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

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []
        if self.args['noup']:
            dimensions = 'p/760x1013'
        else:
            dimensions = 'p/3040x4052'

        for target in self.args['targets'][self.ID]:
            if '/p/' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(self.parser.regex_sub(r'p/\d+x\d+', dimensions, target.replace('dm.', 'www.')))
            else:
                # NOTE: version is there too if needed; used to be V6.
                for path in self.parser.extract_by_regex(self.get(target).content, r'(?<="path":")page/[^"]+'):
                    response = self.parser.load_json(self.get(f'{self.API_URL_BASE}/products/v8/{self.parser.dequery(path)}?activeCountry=US').content)
                    if 'product' in response:
                        products = response['product'].get('productData', '')
                        for product in products:
                            choices = products[product].get('choices', '')
                            for choice in choices:
                                images = choices[choice].get('images', '')
                                for image in images:
                                    urls.append(f'{self.URL_BASE}/p/{dimensions}/{image["image"]}.jpg')

            self.delay()

        for url in urls:
            if '_OF_' not in url: # skip product images
                self.collect(url)

        self.loot()
