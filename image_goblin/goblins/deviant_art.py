import re

from goblins.meta import MetaGoblin


class DeviantArtGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'deviant art goblin'
    ID = 'deviantart'
    URL_PAT = r'(?<=og:image"\scontent=")https?://images-wixmp[^"\s]+'

    def __init__(self, args):
        super().__init__(args)

    def trim(self, url):
        '''remove cropping'''
        return re.sub(r'/v1/[^\?]+(?=\?)', '', url)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if '.jpg' in target:
                urls = [target]
            else:
                urls = self.extract_by_regex(self.URL_PAT, target)
            for url in urls:
                self.collect(self.trim(url),
                             filename=re.sub(r'_[a-z\d]+-pre', '', self.parser.extract_filename(url)))
        self.loot()
