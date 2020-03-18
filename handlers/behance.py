import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class BehanceGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    link types:
        - image
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, tickrate, verbose, nodl)
        self.mode = mode
        self.img_pat = r'https://mir-s3-cdn-cf.behance.net/project_modules/[\w/\.]+\.[A-Za-z]+'
        self.size_pat = r'1400(_opt_1)*|max_1200|disp'
        self.sizes = ('max_3840', 'fs', '1400', 'max_1200', 'disp')
        print(f'[{self.__str__()}] <running>')

    def __str__(self):
        return 'behance goblin'

    def crop(self, url, size):
        return re.sub(self.size_pat, size, self.url)

    def run(self):
        if self.mode == 'iter':
            links = self.read_file(self.external_links, True)
        else:
            links = [self.url]
        for link in links:
            for size in self.sizes:
                attempt = self.loot(self.crop(link, size), self.path_main)
                if attempt:
                    break
                sleep(self.tickrate)
