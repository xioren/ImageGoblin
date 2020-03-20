import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class YandyGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    link types:
        - web page
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        self.mode = mode
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'yandy goblin'

    def run(self):
        html = self.get_html(self.url)
        for link in {l.group() for l in re.finditer(r'https://assets.yandycdn.com/Products/[^-]+-\d+.jpg', html)}:
            self.loot(link.replace('Products', 'HiRez'))
            sleep(self.tickrate)
