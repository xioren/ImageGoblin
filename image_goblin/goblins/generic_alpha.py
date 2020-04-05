import re
from goblins.meta import MetaGoblin


class AlphaGoblin(MetaGoblin):

    '''
    handles: Magento (media/catalog)
    docs: https://docs.magento.com/m2/ee/user_guide/catalog/product-image-resizing.html
    accepts:
        - webpage
    generic back-end for:
        - agent provocateur
        - bikini lovers
        - blush
        - maison close
        - only hearts
        - simone perele
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https*\:[^" \n]+media[^" \n]+\.jpe*g'
        self.clean=True

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'media/catalog' in target:
                urls = []
                if not self.args['silent']:
                    print(f'[{self.__str__()}] <WARNING> url type not supported')
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                self.collect(re.sub(r'cache/(\d/\w+/(\d+x(\d+)*/)*)*\w+/', '', url.replace('\\', '')), clean=self.clean)
        self.loot()
