import re

from goblins.meta import MetaGoblin

# TODO: add site specific iteration and scannable flag

class ShopifyGoblin(MetaGoblin):
    '''accepts:
        - image*
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
        self.url_pat = r'cdn\.shopify\.com/s/files/[^" \n]+((\w+-)+)?\d+x(\d+)?[^" \n]+'

    def trim(self, url):
        '''remove alternate file hash'''
        return re.sub(r'_[a-z\d]+(\-[a-z\d]+){4}', '', url)

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'cdn.shopify' in target:
                urls = [target]
                self.logger.log(1, self.__str__(), 'WARNING', 'image urls not fully supported')
            else:
                urls = self.extract_urls_greedy(self.url_pat, target)
            for url in urls:
                if self.args['noupgrade']:
                    self.collect(url, clean=True)
                else:
                    self.collect(self.trim(url), clean=True)
        self.loot()
        self.cleanup(self.path_main)
