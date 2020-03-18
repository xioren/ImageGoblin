import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class GettyGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    link types:
        - image
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, tickrate, verbose, nodl)
        self.mode = mode
        print(f'[{self.__str__()}] <running>')

    def __str__(self):
        return 'getty goblin'

    def upgrade(self, image):
        id = re.search(r'\d+', image).group()
        return f'https://media.gettyimages.com/photos/picture-id{id}?s=2048x2048'

    def run(self):
        if self.mode == 'iter':
            links = self.read_file(self.external_links, True)
        else:
            links = [self.url]
        for link in links:
            self.loot(self.upgrade(link), self.path_main)
            sleep(self.tickrate)
