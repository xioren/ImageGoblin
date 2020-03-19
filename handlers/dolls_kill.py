import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class DollsKillGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    link types:
        - web pag
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, tickrate, verbose, nodl)
        self.mode = mode
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'dolls kill goblin'

    def run(self):
        html = self.get_html(self.url)
        for link in {l.group() for l in re.finditer(r'img src="https://media.dollskill.com[^"]+\-\d+.jpg', html)}:
            self.loot(re.sub(r'\d+.jpg', '1.jpeg', link).replace('img src="', ''))
            sleep(self.tickrate)
