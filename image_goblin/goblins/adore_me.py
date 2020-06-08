import re
import json

from goblins.meta import MetaGoblin


class AdoreMeGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'adore me goblin'
    ID = 'adoreme'
    API_URL = 'https://www.adoreme.com/v7/catalog/products/permalink'

    def __init__(self, args):
        super().__init__(args)

    def extract_slug(self, url):
        '''extract slug from url'''
        return self.parser.dequery(url).rstrip('/').split('/')[-1]

    def run(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'media-resize' in target:
                urls.append(target)
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
            else:
                slug = self.extract_slug(target)
                response = json.loads(self.get(f'{self.API_URL}/{slug}').content)

                # NOTE: other colors are located in related products

                for image in response.get('gallery', ''):
                    urls.append(image['url'])

            self.delay()

        for url in urls:
            self.collect(re.sub(r'(?<=resize/)[^/]+', '0', url), filename=re.search(r'[^/]+(?=/full)', url).group())

        self.loot()
