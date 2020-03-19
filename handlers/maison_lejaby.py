import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class MaisonLejabyGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    link types:
        - image
        - web page
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, tickrate, verbose, nodl)
        self.mode = mode
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'maison lejaby goblin'

    def run(self):
        if '.html' in self.url:
            links = {l.group() for l in re.finditer(r'https://www\.maisonlejaby\.com.+\.jpg', self.get_html(self.url))}
        else:
            links = [self.url]
        for link in links:
            link = re.sub(r'[A-Z]\.jpg', '', link).replace('medium', 'large')
            for char in ('A', 'B', 'C', 'D', 'E', 'F'):
                self.loot(f'{link}{char}.jpg')
                sleep(self.tickrate)
