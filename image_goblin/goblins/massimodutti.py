from goblins.generic_delta import DeltaGoblin

# QUESTION: remove everything after initial query?

class MassimoDuttiGoblin(DeltaGoblin):

    NAME = 'massimo dutti goblin'
    ID = 'massimodutti'
    SIZE = 0
    API_URL = 'https://www.massimodutti.com/itxrest/2/catalog/store/34009527/30359506/category/0/product/{}/detail'
    URL_BASE = 'https://static.massimodutti.net/3/photos'
    MODIFIERS = [f'_{j}_{k}_' for j in range(1, 8) for k in range(1, 7)]

    def __init__(self, args):
        super().__init__(args)

    def extract_urls(self, url):
        '''extract urls from html'''
        return self.parser.extract_by_regex(self.get(url).content, self.URL_PAT)
