import re
from handlers.meta_goblin import MetaGoblin


class YandyGoblin(MetaGoblin):

    '''
    accepts:
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'yandy goblin'

    def run(self):
        if 'assets.yandycdn' in self.args['url']:
            links = []
            if not self.args['silent']:
                print(f'[{self.__str__()}] <WARNING> url type not supported')
        else:
            links = self.extract_links(r'https://assets.yandycdn.com/Products/[^-]+-\d+.jpg', self.args['url'])
        for link in links:
            self.collect(link.replace('Products', 'HiRez'))
        self.loot()
