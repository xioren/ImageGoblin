import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class GettyGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    link types:
        - image
        - webpage
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        self.mode = mode
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'getty goblin'

    def upgrade(self, image):
        id = re.search(r'id\d+', image).group()
        return f'https://media.gettyimages.com/photos/picture-{id}?s=2048x2048'

    def run(self):
        if 'media' in self.url:
            self.loot(self.upgrade(self.url))
        else:
            links = {l.group() for l in re.finditer(r'https*[^"]+id\d+', self.get_html(self.url))}
            for link in links:
                self.loot(self.upgrade(link))
                sleep(self.tickrate)
