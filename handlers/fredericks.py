import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class FredericksGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    link types:
        - image
    # BUG: does not get all imaged ---> javascript
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, tickrate, verbose, nodl)
        self.mode = mode
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'fredericks goblin'

    def run(self):
        html = self.get_html(self.url)
        for parsed in {p.group() for p in re.finditer(r'//[^" \n]+\.jpe*g', html)}:
            self.loot(re.sub(r'\.\d+w.jpg', r'\.jpg', parsed))
            sleep(self.tickrate)
