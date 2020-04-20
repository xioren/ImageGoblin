import re

from goblins.meta import MetaGoblin

# BUG: currently getting gzip EOF errors

class BrownieGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https?://www\.browniespain\.com/\d+-thickbox_default/[a-z\d\-]+\.jpg'

    def __str__(self):
        return 'brownie goblin'

    def __repr__(self):
        return 'brownie'

    def extract_id(self, url):
        return re.search(r'(?<=\.com/)\d+', url).group()

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if '.jpg' in target:
                urls = [target]
                self.logger.log(1, self.__str__(), 'WARNING', 'image urls not fully supported')
            else:
                urls = self.extract_urls_greedy(self.url_pat, target)
            for url in urls:
                id = self.extract_id(url)
                self.collect(url.replace('-thickbox_default', ''), filename=id)
        self.loot()
