from goblins.meta import MetaGoblin


class FlickrGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'flickr goblin'
    ID = 'flickr'
    URL_PAT = r'live\.staticflickr\.com[\\/\d]+_[a-z\d]+_o\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')

        for target in self.args['targets'][self.ID]:
            if 'staticflickr' in target:
                urls = [target]
            else:
                urls = self.parser.extract_by_regex(self.get(target).content, self.URL_PAT)

            for url in urls:
                self.collect(url)

        self.loot()
