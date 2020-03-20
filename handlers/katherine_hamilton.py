import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class KatherineHamiltonGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    link types:
        - image
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        self.mode = mode
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'katherine hamilton goblin'

    def run(self):
        if '.jpg' in self.url:
            pass
        else:
            self.url = re.search(r'https*[^" \n]+\.jpg', self.get_html(self.url)).group()
        self.url = (re.sub(r'(-front|-back)*(\d+x\d+)*\.jpg', '', self.url)).strip('-')
        for view in ('', '-front', '-back', '-side', '-set', '-fton', '-open', '-fron-1'):
            self.loot(f'{self.url}{view}.jpg')
            sleep(self.tickrate)
