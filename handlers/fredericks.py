import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class FredericksGoblin(MetaGoblin):

    '''
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'fredericks goblin'

    def run(self):
        if 'cloudfront' in self.args['url']:
            # NOTE: does not scan
            links = [self.args['url']]
        else:
            # links = self.extract_links(r'//[^" \n]+\.jpe*g', self.args['url'])
            links = []
            if not self.args['silent']:
                print(f'[{self.__str__()}] <WARNING> url type not supported')
        for link in links:
            self.loot(re.sub(r'\.\d+w', '', link))
            sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
