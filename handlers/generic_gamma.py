import re
from time import sleep
from parsing import *
from handlers.meta_goblin import MetaGoblin

# removing /dw/image/v2/AAYL_PRD give original image, while leaving it in allow resizing
# TODO: handle both image and webpage urls

class GammaGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    url types:
        - image
    generic backend for:
        - boux avenue
        - etam
        - sandro
        - springfield
        - womens secret
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, tickrate, verbose, nodl)
        self.mode = mode

    def extract_id(self, url):
        return re.search(self.pattern, url).group()

    def prep(self, url):
        if 'images' in url:
            return re.sub(r'dw/image/v\d/[A-Z]+_[A-Z]+/', '', re.sub(r'default/\w+/', 'default/images/', url))
        else:
            return re.sub(r'dw/image/v\d/[A-Z]+_[A-Z]+/', '', re.sub(r'default/\w+/', 'default/', url))

    def run(self):
        id = self.extract_id(self.url)
        self.url = dequery(self.prep(re.sub(fr'{id}(\w+)*.jpg', '', self.url)))
        for mod in self.modifiers:
            self.loot(f'{self.url}{id}{mod}.jpg')
            sleep(self.tickrate)
