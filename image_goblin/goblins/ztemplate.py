from goblins.meta import MetaGoblin


class Goblin(MetaGoblin):
    '''accepts:
        -
    '''

    NAME = ' goblin'
    ID = ''
    URL_PAT = r''

    def __init__(self, args):
        super().__init__(args)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if '' in target:
                urls = [target]
            else:
                urls = self.extract_by_regex(target)
            for url in urls:
                self.collect(url)
        self.loot()
