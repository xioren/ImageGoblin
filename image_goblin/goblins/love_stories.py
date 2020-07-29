from goblins.meta import MetaGoblin


class LoveStoriesGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'love stories goblin'
    ID = 'lovestories'
    URL_PAT = r'https://lovestories\.xcdn\.nl/[\w,]+/-/catalog/product/[^\.]+\.jpg'
    URL_BASE = 'https://lovestories.xcdn.nl/FD/-/catalog/product'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        return self.parser.regex_search(r'[a-z\d]+(?=_[a-z]\d\.jpg)', url)

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'xcdn' in target:
                urls.append(target)
            else:
                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

            self.delay()

        for url in urls:
            id = self.extract_id(url)
            for n in range(1, 6):
                self.collect(f'{self.URL_BASE}/{id[0]}/{id[1]}/{id}_m{n}.jpg')

        self.loot()
