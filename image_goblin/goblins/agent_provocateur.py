import json

from goblins.meta import MetaGoblin


# NOTE: used to use Magento API


class AgentProvocateurGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'agent provocateur goblin'
    ID = 'agentprovocateur'
    API_URL = 'https://www.agentprovocateur.com/api/n/bundle'
    BASE_URL = 'https://www.agentprovocateur.com'

    def __init__(self, args):
        super().__init__(args)

    def extract_path(self, url):
        '''return relative url path'''
        return self.parser.dequery(url).split('#')[0].split('/')[-1]

    def isolate(self, url):
        '''isolate original url from processed url'''
        if 'tco-images' in url:
            return url.split(')/')[-1]
        return url

    def run(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'media/catalog' in target:
                base = self.isolate(target).split('_')[0]

                for n in range(1, 6):
                    urls.append(f'{base}_ecom_{n}.jpg')
            else:
                self.headers.update({'Content-Type': 'application/json'})
                POST_DATA = json.dumps(
                    {
                        "requests":
                            [
                                {
                                    "action":"route",
                                     "children":
                                        [
                                            {
                                                "path":f"/{self.extract_path(target)}",
                                                "_reqId":0
                                            }
                                        ]
                                }
                            ]
                        }
                    )

                response = json.loads(self.post(self.API_URL, data=POST_DATA).content)

                if 'catalog' in response:
                    for entry in response['catalog']:
                        if 'media' in entry:
                            for image in entry['media']:
                                urls.append(f'{self.BASE_URL}/static/media/catalog{image["image"]}')

        for url in urls:
            if 'flatshot' in url: # skip product images
                continue

            self.collect(url)

        self.loot()
