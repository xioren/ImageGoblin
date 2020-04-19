import re

from goblins.meta import MetaGoblin


class SsenseGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https?://(img\.ssensemedia|res\.cloudinary)\.com/(images?|ssenseweb)/[^" ]+'

    def __str__(self):
        return 'ssense goblin'

    def __repr__(self):
        return 'ssense'

    def extract_id(self, url):
        '''extract image id from url'''
        return re.search(r'[A-Z\d]+(?=_\d)', url).group()

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'img.ssensemedia' in target or 'res.cloudinary' in target:
                urls = [target]
            else:
                urls = self.extract_urls_greedy(self.url_pat, target)
            for url in urls:
                id = self.extract_id(url)
                for n in range(6):
                    self.collect(f'https://img.ssensemedia.com/images/{id}_{n}/{id}_{n}.jpg')
        self.loot()
