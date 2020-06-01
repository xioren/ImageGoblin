import re
import json

from goblins.meta import MetaGoblin

# NOTE: same as monster

class FrancinaGoblin(MetaGoblin):
    '''accepts:
        - webpage
    '''

    NAME = 'francina models goblin'
    ID = 'francina'
    API_URL = 'https://francinamodels.com/api/models/details'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        '''extract model id from url'''
        return url.split('-')[1].split('/')[-1]

    def run(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            model_id = self.extract_id(target)

            response = json.loads(self.get(f'{self.API_URL}/{model_id}').content)

            if 'ActiveBook' in response:
                for page in response['ActiveBook']['Pages']:
                    urls.append(page['Picture']['URL'])
            # NOTE: video book present in json but not used

        for url in urls:
            self.collect(url)

        self.loot()
