import re
from time import sleep
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

    def __str__(self):
        return 'katherine hamilton goblin'

    def run(self):
        if '.jpg' in self.args['url']:
            links = []
            print(f'[{self.__str__()}] <WARNING> url type not supported')
        else:
            links = self.extract_links(r'https*[^" \n]+\.jpg', self.args['url'])
        for link in links:
            link = re.sub(r'(-front|-back)*(\d+x\d+)*\.jpg', '', link).strip('-')
            for view in ('', '-front', '-back', '-side', '-set', '-fton', '-open', '-fron-1'):
                self.loot(f'{link}{view}.jpg')
                sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
