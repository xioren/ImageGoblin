from meta import MetaGoblin

# NOTE: api works sometimes...depends on product id
# TODO: find solution
# legacy: https://www.trendyol.com/assets/product/media/images/20191021/17/449253/57309150/5/5_org_zoom.jpg

class TrendyolGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'trandyol goblin'
    ID = 'trendyol'
    # API_URL = 'https://api.trendyol.com/webbrowsinggw/api/productDetails'
    # IMG_BASE = 'https://cdn.dsmcdn.com'

    def __init__(self, args):
        super().__init__(args)

    def extract_base(self, url):
        '''extract base of url'''
        return self.parser.regex_sub(r'\d+/\d+_[a-z]+(_[a-z]+)?\.jpg', '', url)

    # def extract_id(self, url):
    #     '''extract product id'''
    #     return self.parser.regex_search(r'(?<=p-)\d+', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            self.logger.log(2, self.NAME, 'looting', target)
            self.logger.spin()

            if 'img-trendyol' in target or 'cdn.dsmcdn' in target:
                urls.append(target)
            else:
                self.logger.log(2, self.NAME, 'WARNING', 'webpage urls not supported', once=True)

            self.delay()

        for url in urls:
            url_base = self.extract_base(url)

            for n in range(1, 10):
                # TODO: ty\d+ is not constant. find better approach
                self.collect(f'{url_base}{n}/{n}_org_zoom.jpg', filename=f'{url_base.split("/")[-2]}_{n}_org_zoom')

        self.loot()
