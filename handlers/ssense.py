import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


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

    def extract_id(self, url):
        return re.search(r'[A-Z\d]+_\d', url).group()[:-2]

    def run(self):
        if '' in self.args['url']:
            links = [self.args['url']]
        else:
            # NOTE: does not work ----> javascript
            links = self.extract_links(r'https*://img\.ssensemedia\.com/images*/[^" ]', self.args['url'])
        for link in links:
            id = self.extract_id(link)
            for n in range(6):
                self.loot(f'https://img.ssensemedia.com/images/{id}_{n}/{id}_{n}.jpg')
            sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
