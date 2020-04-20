import re

from goblins.generic_omega import MetaGoblin

# NOTE: can use gamma goblin but has no real conistancy with filenames or urls

# FIXME: does not work

class WolfordGoblin(MetaGoblin):
    '''accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'wolford goblin'

    def __repr__(self):
        return 'wolford'

    def trim(self, url):
        '''strip cropping from url'''
        return re.sub(r'default/\w+/images', 'default/images', url).replace('dw/image/v2/BBCH_PRD/', '')

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'demandware' in target:
                urls = [target]
            else:
                urls = []
                self.logger.log(1, self.__str__(), 'WARNING', 'webpage urls not supported')
            for url in urls:
                url = self.trim(url)
                if 'Additional-Picture' in url:
                    for n in range(1, 4):
                        self.collect(f'{url[:-5]}{n}.JPG')
                else:
                    self.collect(url)
        self.loot()
