from goblins.meta import MetaGoblin


class FlickrGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'live\.staticflickr.com\\/\d+\\/\d+_[a-z0-9]+_o\.jpg'

    def __str__(self):
        return 'flickr goblin'

    def __repr__(self):
        return 'flickr'

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'staticflickr' in target:
                urls = [target]
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                self.collect(url)
        self.loot()
