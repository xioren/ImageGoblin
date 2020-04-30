import re

from goblins.meta import MetaGoblin


class TisjaDamenGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'tisja damen goblin'
    ID = 'tisjadamen'
    URL_PAT = r'/images/magictoolbox_cache/[^" ]+\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def trim(self, url):
        '''seperate image from rest url'''
        return re.search(r'(?<=/)[^/]+$', url).group()

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'images' in target:
                urls = [target]
                self.logger.log(1, self.NAME, 'WARNING', 'image urls not fully supported')
            else:
                urls = self.extract_by_regex(self.URL_PAT, target)
            for url in urls:
                image = self.trim(url)
                for n in range(1, 4):
                    self.collect(f'https://tisjadamen.com/images/detailed/{n}/{image}')
        self.loot()
