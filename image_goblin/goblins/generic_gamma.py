import re

from goblins.meta import MetaGoblin

# NOTE: scaling with q=100 gives higher resolution; investigate.

class GammaGoblin(MetaGoblin):
    '''handles: Demandware
    docs: https://documentation.b2c.commercecloud.salesforce.com/DOC1/index.jsp
    --> dw.content --> MediaFile
    accepts:
        - image
        - webpage
    generic backend for:
        - boux avenue
        - etam
        - jennyfer
        - livy
        - marlies dekkers
        - sandro
        - springfield
        - vila
        - womens secret
    '''

    URL_PAT = r'[^"\s;]+demandware[^"\s;]+\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def extract_parts(self, url):
        '''split the url into id, end'''
        return re.split(self.ITER_PAT, url)

    def isolate(self, url):
        '''isolate the end of the url'''
        return re.search(r'(?<=/)[^/]+\.jpe?g', url).group()

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'demandware' in target:
                urls = [target]
            else:
                urls = self.extract_by_regex(self.URL_PAT, target)
            for url in urls:
                if not re.search(f'(?:{self.IMG_PAT})', url):
                    continue
                id, url_end = self.extract_parts(self.isolate(url))
                for mod in self.MODIFIERS:
                    self.collect(f'{self.URL_BASE}{id}{mod}{self.parser.dequery(url_end)}')
        self.loot()
