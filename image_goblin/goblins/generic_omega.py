import re
import os
from goblins.meta_goblin import MetaGoblin


class OmegaGoblin(MetaGoblin):

    '''
    handles: all urls that did not match a specific goblin
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = fr'(<img[^<>]+src="[^" ;\']+)|((https?://)?[^"\n \';]+{self.filetypes}({self.query_pat})?)'

    def __str__(self):
        return 'generic goblin'

    def __repr__(self):
        return 'generic'

    def find_urls(self, url):
        '''
        extract media urls from html
        '''
        urls = self.extract_urls(self.url_pat, url)
        cleaned_urls = [re.sub(r'<img.+src="', '', url) for url in urls]
        for url in cleaned_urls:
            if re.search(self.filter_pat, url):
                continue
            if self.args['format']:
                url = self.user_format(url)
            self.collect(url)

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if re.search(r'\.(jpe?g|png|gif|webp|tiff?)', target, re.IGNORECASE):
                if self.args['format']:
                    target = self.user_format(target)
                self.collect(target)
            else:
                self.find_urls(target)
            self.loot()
        if not self.args['nodl'] and not self.args['noclean']:
            self.cleanup(self.path_main)
