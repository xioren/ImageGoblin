import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class ShopifyGoblin(MetaGoblin):

    '''
    accepts:
        - webpage
    generic back-end for:
        - bluebella
        - bordelle
        - caro swim
        - cecilie copenhagen
        - dora larsen
        - else
        - fashion nova
        - five dancewear
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
        self.clean = True
        self.image_pat = r'cdn.shopify.com/[^" \n]+((\w+-)+)*\d+x(\d+)*[^" \n]+'

    # TODO: add shopify __str__ for non matched inputs?

    def trim(self, url):
        # NOTE: changed to 4 instead of +...check if always 4 with different urls
        return re.sub(r'_[a-z\d]+(\-[a-z\d]+){4}', '', url)

    def run(self):
        links = {p.group() for p in re.finditer(self.image_pat, self.get_html(self.args['url']))}
        for link in links:
            # TODO: fix this to be specific to trim (or whatevr arguemnt is passed)
            if self.args['format']:
                self.loot(self.trim(link), clean=True)
            else:
                self.loot(link, clean=True)
            sleep(self.args['tickrate'])
        # if self.clean and not self.args['nodl']:
        #     self.cleanup(self.path_main)
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
