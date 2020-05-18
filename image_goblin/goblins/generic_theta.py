import re

from goblins.meta import MetaGoblin

# TODO: add site specific iteration and scannable flag

class ThetaGoblin(MetaGoblin):
    '''handles: shopify
    docs: https://help.shopify.com/en/manual/products/product-media
    accepts:
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
        - hanne bloch
        - kiki de montparnasse
        - lounge
        - skatie
        - skin
        - the great eros
        - triangl
        - underprotection
        - vitamin a
    '''

    NAME = 'theta goblin'
    ID = 'theta'
    URL_PAT = r'cdn\.shopify\.com/s/files/[^"\s\n]+((\w+-)+)?\d+x(\d+)?[^"\s\n]+'

    def __init__(self, args):
        super().__init__(args)

    def trim(self, url):
        '''remove variant hash'''
        return re.sub(r'_[a-z\d]+(\-[a-z\d]+){4}', '', url)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')

        for target in self.args['targets'][self.ID]:
            if 'cdn.shopify' in target:
                urls = [target]
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
            else:
                urls = self.parser.extract_by_regex(self.get(target).content, self.URL_PAT)

            for url in urls:
                if self.args['noup']:
                    self.collect(url, clean=True)
                else:
                    self.collect(self.trim(url), clean=True)

        self.loot()
        self.cleanup(self.path_main)
