import re

from goblins.meta import MetaGoblin


class TisjaDamenGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'/images/magictoolbox_cache/[^" ]+\.jpg'

    def __str__(self):
        return 'tisja damen goblin'

    def __repr__(self):
        return 'tisjadamen'

    def trim(self, url):
        '''seperate image from rest url'''
        return re.search(r'(?<=/)[^/]+$', url).group()

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'images' in target:
                urls = [target]
                self.logger.log(1, self.__str__(), 'WARNING', 'image urls not fully supported')
            else:
                urls = self.extract_by_regex(self.url_pat, target)
            for url in urls:
                image = self.trim(url)
                for n in range(1, 4):
                    self.collect(f'https://tisjadamen.com/images/detailed/{n}/{image}')
        self.loot()
