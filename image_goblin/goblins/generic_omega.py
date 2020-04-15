import re
import os

from goblins.meta import MetaGoblin


class OmegaGoblin(MetaGoblin):
    '''handles: all urls that did not match a specific goblin
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat_a = r'<img.+?(src|data([^=]+)?)="[^"]+'
        self.url_pat_b = fr'(https?://)?(/[^"\n \';]+)+{self.filetypes}({self.query_pat})?'
        self.url_pat_compounded = f'{self.url_pat_a}|{self.url_pat_b}'

    def __str__(self):
        return 'generic goblin'

    def __repr__(self):
        return 'generic'

    def format(self, url):
        '''format a url either automatically or via user input modifier'''
        if self.args['format']:
            return self.user_format(url)
        elif not self.args['noupgrade']:
            return self.auto_format(url)
        else:
            return url

    def find_urls(self, url):
        '''extract image urls from html'''
        print(f'[{self.__str__()}] <parsing urls>')
        urls = self.extract_urls(self.url_pat_compounded, url)
        cleaned_urls = [re.sub(r'<img[^<>]+="', '', url) for url in urls]
        for url in cleaned_urls:
            if re.search(self.filter_pat, url, re.IGNORECASE):
                continue
            elif '.php?img=' in url:
                url = url.split('.php?img=')[1]
            self.collect(self.format(url.lstrip('.')))

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if re.search(f'(?:{self.filetypes}|/uploads?/|/images?/)', target, re.IGNORECASE):
                self.collect(self.format(target))
            else:
                self.find_urls(target)
        self.loot()
        if not self.args['nodl'] and not self.args['noclean']:
            self.cleanup(self.path_main)
