from meta import MetaGoblin


class GiselaGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'gisela goblin'
    ID = 'gisela'
    API_URL = 'https://apiwww.gisela.com/v1/models'
    IMG_URL = 'https://static.gisela.com/assets/img'

    def __init__(self, args):
        super().__init__(args)

    def extract_slug(self, url):
        return self.parser.regex_search(r'[\w\-]+(?=.html)', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            self.logger.log(2, self.NAME, 'looting', target)
            self.logger.spin()
            
            if 'assets/img' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(target)
            else:
                slug = self.extract_slug(target)
                self.headers.update({'Origin': 'https://www.gisela.com',
                                     'Accept-Language': 'en-US,en'})

                response = self.parser.load_json(self.get(f'{self.API_URL}/{slug}.html?category={slug}').content)

                if 'model' in response:
                    for image in response['model']['images']:
                        urls.append(f'{self.IMG_URL}/{image["path"]}/original/{image["file"]}')

            self.delay()

        for url in urls:
            self.collect(url)

        self.loot()
