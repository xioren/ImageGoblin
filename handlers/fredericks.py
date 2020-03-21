import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class FredericksGoblin(MetaGoblin):

    '''
    accepts:
        - image
    # BUG: does not get all images ---> javascript
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'fredericks goblin'

    def run(self):
        for link in self.extract_links(r'//[^" \n]+\.jpe*g', self.args['url']):
            self.loot(re.sub(r'\.\d+w.jpg', r'\.jpg', link))
            sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
