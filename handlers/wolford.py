import re
from handlers.generic_omega import MetaGoblin

# NOTE: can use gamma goblin but has no real conistancy with filenames or urls formats

class WolfordGoblin(MetaGoblin):

    '''
    accepts:
        - url
    '''

    def __init__(self, args):
        super().__init__(args)
        self.modifiers = ('1', '2', '3', '4')
        self.pattern = r'\d+_\d+_'
        # NOTE: this seems season specific, does it change?
        self.base = 'https://www.wolfordshop.com/on/demandware.static/-/Sites-wolfordb2c-catalog/default/SS20/'

    def __str__(self):
        return 'wolford goblin'

    def prep(self, url):
        return re.sub(r'default/\w+/images', 'default/images', url).replace('dw/image/v2/BBCH_PRD/', '')

    def run(self):
        if 'demandware' in self.args['url']:
            links = [self.args['url']]
        else:
            links = []
            if not self.args['silent']:
                print(f'[{self.__str__()}] <WARNING> url type not supported')
        for link in links:
            link = self.prep(link)
            if 'Additional-Picture' in link:
                link = re.sub(r'\d\.JPG', '', link)
                for n in range(1, 4):
                    self.collect(f'{link}{n}.JPG')
            else:
                self.collect(link)
        self.loot()
