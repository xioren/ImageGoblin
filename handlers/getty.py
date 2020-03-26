import re
from handlers.meta_goblin import MetaGoblin


class GettyGoblin(MetaGoblin):

    '''
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'getty goblin'

    def upgrade(self, image):
        id = re.search(r'id\d+', image).group()
        return f'https://media.gettyimages.com/photos/picture-{id}?s=2048x2048'

    def run(self):
        if 'media' in self.args['url']:
            self.loot(self.upgrade(self.args['url']))
        else:
            links = self.extract_links(r'https*[^"]+id\d+', self.args['url'])
            for link in links:
                self.collect(self.upgrade(link))
        self.loot()
