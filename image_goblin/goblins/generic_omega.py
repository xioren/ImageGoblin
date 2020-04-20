import re

from goblins.meta import MetaGoblin


class OmegaGoblin(MetaGoblin):
    '''handles: all urls that did not match a specific goblin
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = re.compile(fr'(https?://)?[^"\n \';]+{self.parser.filetypes}([\?&][^" ]+$)?',
                                  flags=re.IGNORECASE)
        self.filter_pat = re.compile(r'\.(js|css|pdf|php|html)|(fav)?icon|logo|menu',
                                     flags=re.IGNORECASE)

    def __str__(self):
        return 'generic goblin'

    def __repr__(self):
        return 'generic'

    def format(self, url):
        '''format a url either automatically or via user input modifier'''
        if self.args['format']:
            return self.parser.user_format(url)
        elif not self.args['noupgrade']:
            return self.parser.auto_format(url)
        else:
            return url

    def find_urls(self, url):
        '''find and collect urls'''
        urls = self.extract_urls(url)
        for url in urls:
            self.collect(self.format(url))

    def find_urls_greedy(self, url):
        '''greedily find and collect urls'''
        urls = self.extract_urls_greedy(self.url_pat, url)
        for url in urls:
            if re.search(self.filter_pat, url):
                continue
            elif '.php?img=' in url:
                url = url.split('.php?img=')[1]
            self.collect(self.format(url.lstrip('.')))

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if re.search(f'(?:{self.parser.filetypes}|/upload/|/image/)', target, re.IGNORECASE):
                self.collect(self.format(target))
            else:
                if self.args['greedy']:
                    self.find_urls_greedy(target)
                else:
                    self.find_urls(target)
        self.loot()
        self.cleanup(self.path_main)
