import re

from goblins.meta import MetaGoblin

# NOTE: scaling with q=100 gives higher resolution; investigate.
# TODO: this could really use a better approach

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
        - intimissimi
        - jennyfer
        - livy
        - marlies dekkers
        - sandro
        - springfield
        - tezenis
        - vila
        - womens secret
    '''

    NAME = 'gamma goblin'
    ID = 'gamma'
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
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'demandware' in target:
                urls.append(target)
            else:
                urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

        for url in urls:
            if not re.search(f'(?:{self.IMG_PAT})', url):
                continue

            id, url_end = self.extract_parts(self.isolate(url))
            for mod in self.MODIFIERS:
                self.collect(f'{self.URL_BASE}{id}{mod}{self.parser.dequery(url_end)}{self.QUERY}')

        self.loot()
