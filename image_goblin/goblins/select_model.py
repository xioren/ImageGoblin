import re
import json

from goblins.meta import MetaGoblin


# NOTE: {"query":"{model(slug: \""+model+"\", site: \""+location+"\", siteSolarnetId: "+site_id+") { \n       id\n       }}"}

class SelectGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'select goblin'
    ID = 'select'
    API_URL = 'https://selectmodel.com/graphql'
    SITE_IDS = {'atlanta': '6',
                'chicago': '7',
                'london': '9',
                'los-angeles': '8',
                'miami': '5',
                'milano': '4',
                'model': 'null',
                'paris': '3',
                'stockholm': '2'}

    def __init__(self, args):
        super().__init__(args)

    def extract_location(self, url):
        '''extract location from url'''
        return url.replace('https://', '').split('/')[1]

    def extract_model(self, url):
        '''extract model name from url'''
        return url.rstrip('/').split('/')[-1]

    def run(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'gallery' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(target)
            else:
                model = self.extract_model(target)
                location = self.extract_location(target)
                site_id = self.SITE_IDS[location]
                model_id = re.search(r'(?<=gallery/)\d+|(?<=hero_image_file/)\d+', self.get(target).content).group()

                query = {"query":"{solarnetModel(modelId: "+model_id+", siteSolarnetId: "+site_id+", site: \""+location+"\") { \n        id,\n        firstName,\n        lastName,\n        gender,\n        departmentId,\n        name,\n        slug,\n        bio,\n        image { url },\n        videos { url, type, image { url } },\n        heroImage { sizes { name, url }, orientation, file_dimensions_x, file_dimensions_y },\n        portfolio { url, orientation },\n        polaroids { url },\n        runways { url },\n        covers { url },\n        campaigns { url },\n        books { name, slug, images { url } },\n        measurements { label, value, humanValue, metric, imperial, ukSize },\n        instagram,\n        inTown,\n        uiControls,\n        uiLogoControls,\n        seo { \n        title,\n        description,\n        openGraphTitle,\n        openGraphDescription,\n        openGraphImage,\n        twitterTitle,\n        twitterDescription\n       }\n       }}"}

                response = json.loads(self.post(self.API_URL, data=query).content)

                for image in response['data']['solarnetModel'].get('portfolio', ''):
                    urls.append(image.get('url', ''))

                if response['data']['solarnetModel'].get('polaroids'):
                    for image in response['data']['solarnetModel']['polaroids']:
                        urls.append(image['url'])

                if response['data']['solarnetModel'].get('videos'):
                    for video in response['data']['solarnetModel']['videos']:
                        urls.append(video['url'])

            self.delay()

        for url in urls:
            self.collect(url.replace('expanded_medium/', ''))

        self.loot()
