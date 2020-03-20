import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class PrettyLittleThingGoblin(MetaGoblin):

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
        return 'prettylittlething goblin'

    def run(self):
        html = self.get_html(self.url)
        for parsed in {p.group() for p in re.finditer(r'https://cdn\-img\.prettylittlething\.com[^" \n]+', html)}:
            self.loot(parsed, clean=True)
            sleep(self.tickrate)
