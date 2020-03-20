import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class KatherineHamiltonGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'katherine hamilton goblin'

    def run(self):
        if '.jpg' in self.args['url']:
            pass
        else:
            # QUESTION: should thi be iterative? with finditer?
            self.args['url'] = re.search(r'https*[^" \n]+\.jpg', self.get_html(self.url)).group()
        self.args['url'] = (re.sub(r'(-front|-back)*(\d+x\d+)*\.jpg', '', self.args['url'])).strip('-')
        for view in ('', '-front', '-back', '-side', '-set', '-fton', '-open', '-fron-1'):
            self.loot(f'{self.args["url"]}{view}.jpg')
            sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
