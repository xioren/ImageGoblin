import re

from goblins.meta import MetaGoblin

# BUG: currently getting gzip EOF errors

class BrownieGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'brownie goblin'
    ID = 'brownie'
    URL_PAT = r'https?://www\.browniespain\.com/\d+-thickbox_default/[a-z\d\-]+\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        return re.search(r'(?<=\.com/)\d+', url).group()

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if '.jpg' in target:
                urls = [target]
                self.logger.log(1, self.NAME, 'WARNING', 'image urls not fully supported')
            else:
                urls = self.extract_by_regex(self.URL_PAT, target)
            for url in urls:
                id = self.extract_id(url)
                self.collect(url.replace('-thickbox_default', ''), filename=id)
        self.loot()
