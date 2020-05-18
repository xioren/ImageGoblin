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
    BASE_URL = 'https://www.agentprovocateur.com/static/media/catalog'

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
        self.logger.log(1, self.NAME, 'collecting links')

        for target in self.args['targets'][self.ID]:
            if 'media/catalog' in target:
                urls = []
                base = self.isolate(target).split('_')[0]

                for n in range(1, 6):
                    urls.append(f'{base}_ecom_{n}.jpg')

            else:
                urls = []
                self.headers.update({'Content-Type': 'application/json'})
                POST_DATA = json.dumps(
                                        {
                                            "requests":
                                                [
                                                    {
                                                        "action":"find",
                                                        "type":"block",
                                                        "filter":
                                                            {
                                                                "url":"page-header"
                                                                },
                                                        "verbosity":1,
                                                        "children":
                                                            [
                                                                {
                                                                    "_reqId":0
                                                                }
                                                            ]
                                                    },
                                                    {
                                                        "action":"find",
                                                        "type":"block",
                                                        "filter":
                                                            {
                                                                "url":"page-footer"
                                                            },
                                                        "verbosity":1,
                                                        "children":
                                                            [
                                                                {
                                                                    "_reqId":1
                                                                }
                                                            ]
                                                    },
                                                    {
                                                        "action":"route",
                                                         "children":
                                                            [
                                                                {
                                                                    "path":f"/{self.extract_path(target)}",
                                                                    "_reqId":2
                                                                }
                                                            ]
                                                    }
                                                ]
                                            }
                                        )

                response = json.loads(self.post(self.API_URL, data=POST_DATA).content)

                for entry in response['catalog']:
                    if 'media' in entry:
                        for image in entry['media']:
                            urls.append(f'{self.BASE_URL}{image["image"]}')

            for url in urls:
                self.collect(url)

        self.loot()
