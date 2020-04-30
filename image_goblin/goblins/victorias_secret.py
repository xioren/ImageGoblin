import re

from goblins.meta import MetaGoblin


class VictoriasSecretGoblin(MetaGoblin):
    '''accepts:
        - image*
    '''

    NAME = 'victorias secret goblin'
    ID = 'victoriassecret'
    # URL_PAT = r'https?://www\.victoriassecret\.com/p/[^" ]+\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'victoriassecret.com/p/' in target:
                urls = [target]
                self.logger.log(1, self.NAME, 'WARNING', 'image urls not fully supported')
            else:
                urls = []
                self.logger.log(1, self.NAME, 'WARNING', 'webpage urls not supported')
            for url in urls:
                self.collect(re.sub(r'p/\d+x\d+', 'p/4040x5390', target))
        self.loot()
