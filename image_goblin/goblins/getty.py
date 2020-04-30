import re

from goblins.meta import MetaGoblin


class GettyGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'getty goblin'
    ID = 'getty'
    URL_PAT = r'https?://[^"]+id\d+'

    def __init__(self, args):
        super().__init__(args)

    def upgrade(self, image):
        '''sub in higher resolution cropping'''
        id = re.search(r'id\d+', image).group()
        return f'https://media.gettyimages.com/photos/picture-{id}?s=2048x2048'

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'media' in target:
                urls = [target]
                self.logger.log(1, self.NAME, 'WARNING', 'image urls not fully supported')
            else:
                urls = self.extract_by_regex(self.URL_PAT, target)
            for url in urls:
                self.collect(self.upgrade(url))
        self.loot()
