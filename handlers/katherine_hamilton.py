import re
from handlers.meta_goblin import MetaGoblin


class KatherineHamiltonGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    accepts:
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.link_pat = r'https*[^" \n]+\.jpg'
        self.modifiers = ('', '-front', '-back', '-side', '-set', '-fton', '-open', '-fron-1')

    def __str__(self):
        return 'katherine hamilton goblin'

    def run(self):
        if '.jpg' in self.args['url']:
            links = []
            print(f'[{self.__str__()}] <WARNING> url type not supported')
        else:
            links = self.extract_links(self.link_pat, self.args['url'])
        for link in links:
            link = re.sub(r'(-front|-back)*(\d+x\d+)*\.jpg', '', link).strip('-')
            for mod in self.modifiers:
                self.collect(f'{link}{mod}.jpg')
        self.loot()
