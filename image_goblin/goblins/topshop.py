from goblins.meta import MetaGoblin


class TopshopGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'topshop goblin'
    ID = 'topshop'
    URL_PAT = r'images\.topshop\.com/i/TopShop/[A-Z\d]+_[A-Z]_\d\.jpg'
    QUERY = '?scl=1&qlt=100'

    def __init__(self, args):
        super().__init__(args)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'images.topshop' in target:
                urls = [target]
            else:
                urls = self.extract_by_regex(self.URL_PAT, target)
            for url in urls:
                for n in range(1, 6):
                    self.collect(f'{self.parser.dequery(url)[:-5]}{n}.jpg{self.QUERY}')
        self.loot()
