import re

from goblins.meta import MetaGoblin


class ShopbopGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https?://[a-z\-\.]+amazon\.com[^" ]+\.jpg'

    def __str__(self):
        return 'shopbop goblin'

    def __repr__(self):
        return 'shopbop'

    def prep(self, url):
        '''prepare the url by removing cropping and mobile elements'''
        return re.sub(r'._\w+(_\w+)?_\w+_', '', url).replace('m.media', 'images-na.ssl-images').replace('2-1', '2-0')

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'amazon' in target:
                urls = [target]
            else:
                urls = self.extract_by_regex(self.url_pat, target)
            for url in urls:
                url = self.prep(url)
                for n in range(1, 7):
                    self.collect(re.sub(r'q\d', f'q{n}', url))
        self.loot()
