import re
from handlers.meta_goblin import MetaGoblin

# TODO: add site specific iteration

class ShopifyGoblin(MetaGoblin):

    '''
    accepts:
        - webpage
    generic back-end for:
        - bamba swim
        - bluebella
        - bordelle
        - caro swim
        - cecilie copenhagen
        - dora larsen
        - else
        - fae
        - faithful the brand
        - fashion nova
        - five dancewear
        - fleur du mal
        - for love and lemons
        - fortnight
        - skin
        - the great eros
        - triangl
        - underprotection
        - vitamin a
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'cdn.shopify.com/[^" \n]+((\w+-)+)*\d+x(\d+)*[^" \n]+'

    def trim(self, url):
        # NOTE: changed to 4 instead of +...check if always 4 with different urls
        return re.sub(r'_[a-z\d]+(\-[a-z\d]+){4}', '', url)

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'cdn.shopify' in target:
                urls = []
                if not self.args['silent']:
                    print(f'[{self.__str__()}] <WARNING> url type not supported')
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                # TODO: fix this to be specific to trim (or whatevr arguemnt is passed)
                if self.args['format']:
                    self.collect(self.trim(url), clean=True)
                else:
                    self.collect(url, clean=True)
        self.loot()
        if not self.args['nodl'] and not self.args['noclean']:
            self.cleanup(self.path_main)
