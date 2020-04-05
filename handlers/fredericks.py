import re
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

    def __repr__(self):
        return 'fredericks'

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'cloudfront' in target:
                # NOTE: does not scan
                urls = [target]
            else:
                # urls = self.extract_urls(r'//[^" \n]+\.jpe*g', self.args['url'])
                urls = []
                if not self.args['silent']:
                    print(f'[{self.__str__()}] <WARNING> url type not supported')
            for url in urls:
                self.collect(re.sub(r'\.\d+w', '', url))
        self.loot()
