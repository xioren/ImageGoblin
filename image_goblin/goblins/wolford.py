import re

from goblins.generic_omega import MetaGoblin

# NOTE: can use gamma goblin but has no real conistancy with filenames or urls

class WolfordGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'wolford goblin'
    ID = 'wolford'
    URL_PAT = r'https?://www\.wolfordshop\.com/dw/image/v\d/\w+/on/demandware\.static/-/Sites-\w+-catalog/default/[^"]+'

    def __init__(self, args):
        super().__init__(args)

    def trim(self, url):
        '''strip cropping from url'''
        return re.sub(r'default/\w+/images', 'default/images', self.parser.dequery(url)).replace('dw/image/v2/BBCH_PRD/', '')

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'demandware' in target:
                url.append(target)
            else:
                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

        for url in urls:
            url = self.trim(url)

            if 'Additional-Picture' in url:
                for n in range(1, 4):
                    self.collect(f'{url[:-5]}{n}.JPG')
            else:
                self.collect(url)

        self.loot()
