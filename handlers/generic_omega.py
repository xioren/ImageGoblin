import re
import os
from handlers.meta_goblin import MetaGoblin


class OmegaGoblin(MetaGoblin):

    '''
    handles: all links that did not match a specific handler
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.link_pat = fr'(<img[^<>]+src="[^" ;\']+)|((https?://)?[^"\n \';]+{self.filetypes}({self.query_pat})?)'

    def __str__(self):
        return 'generic goblin'

    def find_links(self):
        '''
        extract media urls from html
        '''
        links = self.extract_links(self.link_pat, self.args['url'])
        cleaned_links = [re.sub(r'<img.+src="', '', link) for link in links]
        for link in cleaned_links:
            if re.search(self.filter_pat, link):
                continue
            if self.args['format']:
                link = self.user_format(link)
            self.collect(link)

    def run(self):
        if re.search(r'\.(jpe?g|png|gif|webp|tiff?)', self.args['url'], re.IGNORECASE):
            if self.args['format']:
                self.args['url'] = self.user_format(self.args['url'])
            self.collect(self.args['url'])
        else:
            self.find_links()
        self.loot()
        if not self.args['nodl'] and not self.args['noclean']:
            self.cleanup(self.path_main)
