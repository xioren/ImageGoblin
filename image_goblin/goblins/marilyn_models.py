import re
import json

from goblins.meta import MetaGoblin


class MarilynGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'marilyn models goblin'
    ID = 'marilyn'
    API_URL = 'http://www.marilynagency.com/api'
    IMAGE_URL = 'https://booker-marilyn.s3.amazonaws.com/library'

    def __init__(self, args):
        super().__init__(args)

    def extract_info(self, url):
        '''extract model, portfolio and polaroid ids'''
        model_id = re.search(r'(?<="id":")\d+', url).group()
        portfolio_id = re.search(r'(?<="portfolioID":")\d+', url).group()
        polaroid_id = re.search(r'(?<="polaID":")\d+', url).group()
        return model_id, portfolio_id, polaroid_id

    def run(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'booker-marilyn' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(target)
            else:
                init_response = self.get(target).content
                model_id, portfolio_id, polaroid_id = self.extract_info(init_response)

                self.headers.update({'X-Requested-With': 'XMLHttpRequest'})

                for item in (portfolio_id, polaroid_id, 'video'):
                    if item == '0':
                        continue

                    response = json.loads(self.get(f'{self.API_URL}/media/1/{model_id}/{item}').content)
                    for item in response:
                        urls.append(f'{self.IMAGE_URL}/{model_id}/{item.get("url", "")}')

            self.delay()

        for url in urls:
            self.collect(url.replace('.jpg', '_M.JPG'))

        self.loot()
