import re
from handlers.meta_goblin import MetaGoblin


class PrettyLittleThingGoblin(MetaGoblin):

    '''
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'prettylittlething goblin'

    def run(self):
        if 'cdn-img.prettylittlething' in self.args['url']:
            links = []
            if not self.args['silent']:
                print(f'[{self.__str__()}] <WARNING> url type not supported')
        else:
            links = self.extract_links(r'https://cdn\-img\.prettylittlething\.com[^" \n]+', self.args['url'])
        for link in links:
            self.collect(link, clean=True)
        self.loot()
