import re
from time import sleep
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
            links = {l.group() for l in re.finditer(r'https*[^"]+id\d+', self.get_html(self.args['url']))}
            for link in links:
                self.loot(self.upgrade(link))
                sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
