import re

from goblins.meta import MetaGoblin


class OmegaGoblin(MetaGoblin):
    '''handles: all urls that did not match a specific goblin
    accepts:
        - image
        - webpage
    '''

    NAME = 'generic goblin'
    ID = 'generic'
    FILETYPES = r'\.(jpe?g|png|gif|mp4|web[pm]|tiff?|mov|svg|bmp|exif)'
    URL_PAT = re.compile(fr'(https?://)?[^"\n \';]+{FILETYPES}([\?&][^" ]+$)?',
                         flags=re.IGNORECASE)
    FILTER_PAT = re.compile(r'\.(js|css|pdf|php|html)|(fav)?icon|logo|menu',
                            flags=re.IGNORECASE)
    ATTR_PAT = re.compile(r'(?:src(?==)|data(?![a-z\-])|data-(src(?!set)|lazy|url)' \
                          r'|content(?![a-z\-])|hires(?![a-z\-]))')
    TAG_PAT = re.compile('(?:ima?ge?|video|source)')

    def __init__(self, args):
        super().__init__(args)


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
        urls = []
        elements = self.extract_by_tag(url)
        for tag in elements:
            if re.search(self.TAG_PAT, tag):
                for attribute in elements[tag]:
                    if re.search(self.ATTR_PAT, attribute):
                        urls.extend(elements[tag][attribute])
        for url in urls:
            self.collect(self.format(url))

    def find_urls_greedy(self, url):
        '''greedily find and collect urls'''
        urls = self.extract_by_regex(self.URL_PAT, url)
        for url in urls:
            if re.search(self.FILTER_PAT, url):
                continue
            elif '.php?img=' in url:
                url = url.split('.php?img=')[1]
            self.collect(self.format(url.replace('\\', '').lstrip('.')))

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if re.search(f'(?:{self.FILETYPES}|/upload/|/image/)', target, re.IGNORECASE):
                self.collect(self.format(target))
            else:
                if self.args['greedy']:
                    self.find_urls_greedy(target)
                else:
                    self.find_urls(target)
        self.loot()
        self.cleanup(self.path_main)
