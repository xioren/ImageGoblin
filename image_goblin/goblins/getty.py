import re

from goblins.meta import MetaGoblin


class GettyGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https?://[^"]+id\d+'

    def __str__(self):
        return 'getty goblin'

    def __repr__(self):
        return 'getty'

    def upgrade(self, image):
        '''sub in higher resolution cropping'''
        id = re.search(r'id\d+', image).group()
        return f'https://media.gettyimages.com/photos/picture-{id}?s=2048x2048'

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'media' in target:
                urls = [target]
                self.logger.log(1, self.__str__(), 'WARNING', 'image urls not fully supported')
            else:
                urls = self.extract_urls_greedy(self.url_pat, target)
            for url in urls:
                self.collect(self.upgrade(url))
        self.loot()
