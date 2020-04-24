from goblins.meta import MetaGoblin


class TopshopGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'images\.topshop\.com/i/TopShop/[A-Z\d]+_[A-Z]_\d\.jpg'
        self.query = '?scl=1&qlt=100'

    def __str__(self):
        return 'topshop goblin'

    def __repr__(self):
        return 'topshop'

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'images.topshop' in target:
                urls = [target]
            else:
                urls = self.extract_by_regex(self.url_pat, target)
            for url in urls:
                for n in range(1, 6):
                    self.collect(f'{self.parser.dequery(url)[:-5]}{n}.jpg{self.query}')
        self.loot()
