import re
from goblins.meta_goblin import MetaGoblin


class GettyGoblin(MetaGoblin):

    '''
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https*[^"]+id\d+'

    def __str__(self):
        return 'getty goblin'

    def __repr__(self):
        return 'annsummers'

    def upgrade(self, image):
        id = re.search(r'id\d+', image).group()
        return f'https://media.gettyimages.com/photos/picture-{id}?s=2048x2048'

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'media' in target:
                # NOTE: does not scan
                self.loot(self.upgrade(target))
            else:
                urls = self.extract_urls(self.url_pat, target)
                for url in urls:
                    self.collect(self.upgrade(url))
        self.loot()
