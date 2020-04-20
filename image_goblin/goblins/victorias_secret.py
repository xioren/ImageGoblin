import re

from goblins.meta import MetaGoblin


class VictoriasSecretGoblin(MetaGoblin):
    '''accepts:
        - image*
    '''

    def __init__(self, args):
        super().__init__(args)
        # self.url_pat = r'https?://www\.victoriassecret\.com/p/[^" ]+\.jpg'

    def __str__(self):
        return 'victorias secret goblin'

    def __repr__(self):
        return 'victoriassecret'

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'victoriassecret.com/p/' in target:
                urls = [target]
                self.logger.log(1, self.__str__(), 'WARNING', 'image urls not fully supported')
            else:
                urls = []
                self.logger.log(1, self.__str__(), 'WARNING', 'webpage urls not supported')
            for url in urls:
                self.collect(re.sub(r'p/\d+x\d+', 'p/4040x5390', target))
        self.loot()
