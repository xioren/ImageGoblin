import re
import json

from time import sleep

from goblins.meta import MetaGoblin


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
        return re.search(r'(?<=com/).+', self.parser.dequery(url).rstrip('/')).group().replace('/', '%2F')

    def run(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'cloudfront' in target:
                self.logger.log(2, self.__str__(), 'WARNING', 'image urls not fully supported', once=True)
                urls.append(target)
            else:
                response = ''

                for _ in range(10):
                    try: # the api is VERY unreliable, usually takes multiple requests to get a proper response.
                        response = json.loads(self.get(self.API_URL + self.QUERY.format(self.extract_page_name(target))).content)
                    except json.decoder.JSONDecodeError:
                        sleep(3)

                if response:
                    for image in response['product'][0]['displayMedia']:
                        urls.append(image['ref'])

        for url in urls:
            self.collect(re.sub(r'\.\d+w', '', url))

        self.loot()
