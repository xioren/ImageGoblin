import re
from goblins.meta_goblin import MetaGoblin

# NOTE: scaling with q=100 gives higher resolution; investigate.

class GammaGoblin(MetaGoblin):

    '''
    handles: Demandware
    docs: https://documentation.b2c.commercecloud.salesforce.com/DOC1/index.jsp
    --> dw.content --> MediaFile
    accepts:
        - image
        - webpage
    generic backend for:
        - boux avenue
        - etam
        - hunkemoller
        - marlies dekkers
        - sandro
        - springfield
        - womens secret
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = fr'[^" ]+demandware[^" ]+\d+_\d\.jpg'

    def extract_parts(self, url):
        iter = re.search(self.iter, url).group()
        id, end = url.split(iter)
        return id, iter, end

    def isolate(self, url):
        return re.search(r'/*[^/]+\.jpe*g', url).group().lstrip('/')

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'demandware' in target:
                urls = [target]
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                id, iter, end = self.extract_parts(self.isolate(url))
                # self.generate_modifiers(iter)
                for mod in self.modifiers:
                    self.collect(f'{self.url_base}{id}{mod}{end}')
        self.loot()
