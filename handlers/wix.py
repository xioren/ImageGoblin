import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class WixGoblin(MetaGoblin):

    '''
    accepts:
        - image
    # TODO: add webpage?
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'wix goblin'

    def run(self):
        self.loot(re.sub(r'\.jpg.+$', '', self.args['url']) + '.jpg')
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
