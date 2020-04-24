import re

from goblins.meta import MetaGoblin


class KatherineHamiltonGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https?://[^" \n]+\.jpg'
        self.modifiers = ('', '-front', '-back', '-side', '-set', '-fton', '-open', '-fron-1')

    def __str__(self):
        return 'katherine hamilton goblin'

    def __repr__(self):
        return 'katherinehamilton'

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if '.jpg' in target:
                urls = []
                self.logger.log(1, self.__str__(), 'WARNING', 'image urls not fully supported')
            else:
                urls = self.extract_by_regex(self.url_pat, target)
            for url in urls:
                url = re.sub(r'(-front|-back)?(\d+x\d+)?\.jpg', '', url).strip('-')
                for mod in self.modifiers:
                    self.collect(f'{url}{mod}.jpg')
        self.loot()
