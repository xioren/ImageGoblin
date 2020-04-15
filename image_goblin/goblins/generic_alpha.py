import re

from goblins.meta import MetaGoblin

# NOTE: stripping _d sometimes works; investigate.

class AlphaGoblin(MetaGoblin):
    '''handles: Magento (media/catalog)
    docs: https://docs.magento.com/m2/ee/user_guide/catalog/product-image-resizing.html
    accepts:
        - image*
        - webpage
    generic back-end for:
        - ami clubwear
        - agent provocateur
        - bikini lovers
        - blush
        - maison close
        - only hearts
        - promise
        - reserved
        - simone perele
        - watercult
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https?:[^" \n]+media\\?/catalog[^" \n]+\.jpe?g'

    def trim_url(self, url):
        '''remove cropping from url'''
        return re.sub(r'/(custom_)?cache.*?(?=/\w/\w/)', '', url)

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'media/catalog' in target:
                if not self.accept_image:
                    urls = []
                    if not self.args['silent']:
                        print(f'[{self.__str__()}] <WARNING> image urls not supported')
                else:
                    urls = self.generate_urls(target)
            else:
                if not self.accept_webpage:
                    urls = []
                    if not self.args['silent']:
                        print(f'[{self.__str__()}] <WARNING> webpage urls not supported')
                else:
                    urls = self.generate_urls(target, False)
            for url in urls:
                self.collect(self.trim_url(url))
        self.loot()
        if not self.args['nodl'] and not self.args['noclean']:
            self.cleanup(self.path_main)
