import re
from goblins.meta import MetaGoblin


class SsenseGoblin(MetaGoblin):

    '''
    mode options:
        -
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'ssense goblin'

    def __repr__(self):
        return 'ssense'

    def extract_id(self, url):
        return re.search(r'[A-Z\d]+_\d', url).group()[:-2]

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'img.ssensemedia' in target:
                urls = [target]
            else:
                # urls = self.extract_urls(r'https*://img\.ssensemedia\.com/images*/[^" ]', self.args['url'])
                urls = []
                if not self.args['silent']:
                    print(f'[{self.__str__()}] <WARNING> url type not supported')
            for url in urls:
                id = self.extract_id(url)
                for n in range(6):
                    self.collect(f'https://img.ssensemedia.com/images/{id}_{n}/{id}_{n}.jpg')
        self.loot()
