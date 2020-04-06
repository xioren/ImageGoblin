import re
from goblins.generic_omega import MetaGoblin

# NOTE: can use gamma goblin but has no real conistancy with filenames or urls

class WolfordGoblin(MetaGoblin):
    '''accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)
        self.modifiers = ('1', '2', '3', '4')
        self.pattern = r'\d+_\d+_'
        # QUESTION: this appears season specific, does it change?
        self.base = 'https://www.wolfordshop.com/on/demandware.static/-/Sites-wolfordb2c-catalog/default/SS20/'

    def __str__(self):
        return 'wolford goblin'

    def __repr__(self):
        return 'wolford'

    def prep(self, url):
        '''strip cropping from url'''
        return re.sub(r'default/\w+/images', 'default/images', url).replace('dw/image/v2/BBCH_PRD/', '')

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'demandware' in target:
                urls = [target]
            else:
                urls = []
                if not self.args['silent']:
                    print(f'[{self.__str__()}] <WARNING> url type not supported')
            for url in urls:
                url = self.prep(url)
                if 'Additional-Picture' in url:
                    url = re.sub(r'\d\.JPG', '', url)
                    for n in range(1, 4):
                        self.collect(f'{url}{n}.JPG')
                else:
                    self.collect(url)
        self.loot()
