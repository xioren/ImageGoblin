import re
from handlers.meta_goblin import MetaGoblin

# QUESTION: keep handler?

class WixGoblin(MetaGoblin):

    '''
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'wix goblin'

    def run(self):
        if '' in self.args['url']:
            # NOTE: does not scan
            links = [self.args['url']]
        else:
            links = []
            if not self.args['silent']:
                print(f'[{self.__str__()}] <WARNING> url type not supported')
        for link in links:
            self.collect(re.sub(r'\.jpg.+$', '', self.args['url']) + '.jpg')
        self.loot()
