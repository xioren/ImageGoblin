from meta import MetaGoblin


# NOTE: some images in form: image-cdn.symphonycommerce.com/images/sites/fredericks/product_images/filename-001.jpg
# these are iterable


class FredericksGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'fredericks goblin'
    ID = 'fredericks'
    API_URL = 'https://www.fredericks.com/api/'
    QUERY = 'page_info?url=%2F{}&params=product'
    # URL_PAT = r'//[^"\s\n]+\.jpe?g'

    def __init__(self, args):
        super().__init__(args)


    def extract_page_name(self, url):
        '''return name of webpage'''
        return self.parser.regex_search(r'(?<=com/).+', self.parser.dequery(url).rstrip('/')).replace('/', '%2F')

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'cloudfront' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(target)
            else:
                response = ''

                for _ in range(10):
                    # the api is VERY unreliable, usually takes multiple requests to get a proper response.
                    response = self.parser.load_json(self.get(self.API_URL + self.QUERY.format(self.extract_page_name(target))).content)
                    if response:
                        break
                    self.delay(3)

                if 'product' in response:
                    for image in response['product'][0].get('displayMedia', ''):
                        urls.append(image['ref'])

            self.delay()

        for url in urls:
            self.collect(self.parser.regex_sub(r'\.\d+w', '', url))

        self.loot()
