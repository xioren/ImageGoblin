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
    URL_PAT = re.compile(fr'[^"\(\'\n\s\[;:]+?/[^"]+?\.jpg(\?[^"\s\n\'\)]+)?', flags=re.IGNORECASE)
    ATTR_PAT = re.compile(r'(?:src(?![a-z])|data(?![a-z\-])|data-(src(?!set)|lazy|url|original)' \
                          r'|content(?![a-z\-])|hires(?![a-z\-]))')
    TAG_PAT = re.compile('(?:a(?![a-z])|ima?ge?|video|source|div)')

    def __init__(self, args):
        super().__init__(args)

    def format(self, url):
        '''format a url either automatically or via user input'''
        if self.args['format']:
            return self.parser.user_format(url)
        elif self.args['noup']:
            return url
        else:
            return self.parser.auto_format(url)

    def find_urls(self, url):
        '''find and collect urls'''
        urls = []
        elements = self.parser.extract_by_tag(self.get(url).content)

        for tag in elements:
            if re.match(self.TAG_PAT, tag):
                for attribute in elements[tag]:
                    if re.match(self.ATTR_PAT, attribute):
                        urls.extend(elements[tag][attribute])

        for url in urls:
            self.collect(self.format(url.replace('\\', '')), filename=self.args['filename'])

    def find_urls_greedy(self, url):
        '''greedily find and collect urls'''
        urls = self.parser.extract_by_regex(self.get(url).content, self.URL_PAT)

        for url in urls:
            if '.php?img=' in url:
                url = url.split('.php?img=')[1]
            self.collect(self.format(url), filename=self.args['filename'])

    def run(self):
        self.logger.log(1, self.NAME, 'collecting urls')

        for target in self.args['targets'][self.ID]:
            if re.search(f'(?:{self.FILETYPES}|/upload/|/image/)', target, re.IGNORECASE):
                self.collect(self.format(target))
            else:
                if self.args['greedy']:
                    self.find_urls_greedy(target)
                else:
                    self.find_urls(target)

            self.delay()

        self.loot()
