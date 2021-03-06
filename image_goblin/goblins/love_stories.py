from meta import MetaGoblin


class LoveStoriesGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'love stories goblin'
    ID = 'lovestories'
    URL_BASE = 'https://lovestories.xcdn.nl/O/-/catalog/product'

    def __init__(self, args):
        super().__init__(args)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')

        for target in self.args['targets'][self.ID]:
            self.logger.log(2, self.NAME, 'looting', target)
            self.logger.spin()

            id = self.parser.regex_search(r'[a-z]\d+', target)
            for n in range(1, 6):
                self.collect(f'{self.URL_BASE}/{id[0]}/{id[1]}/{id}_m{n}.jpg')

        self.loot()
