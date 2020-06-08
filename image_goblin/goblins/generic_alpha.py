import re

from goblins.meta import MetaGoblin

# NOTE: stripping _d sometimes works; investigate.

class AlphaGoblin(MetaGoblin):
    '''handles: Magento API (media/catalog)
    docs: https://docs.magento.com/m2/ee/user_guide/catalog/product-image-resizing.html
    accepts:
        - image*
        - webpage*
    generic back-end for:
        - ami clubwear
        - bikini lovers
        - blush
        - chantelle
        - maison close
        - missy empire
        - only hearts
        - promise
        - reserved
        - simone perele
        - watercult
    '''

    NAME = 'alpha goblin'
    ID = 'alpha'
    URL_PAT = r'https?:[^"\s\n]+media\\?/catalog/product/[^"\s\n]+\.jpe?g'

    def __init__(self, args):
        super().__init__(args)

    def trim(self, url):
        '''remove cropping from url'''
        return re.sub(r'/(custom_)?cache.*?(?=/\w/\w/)', '', url)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'media/catalog' in target:
                if not self.ACCEPT_IMAGE:
                    self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)

                urls.extend(self.generate_urls(target))
            else:
                if not self.ACCEPT_WEBPAGE:
                    self.logger.log(2, self.NAME, 'WARNING', 'webpage urls not supported', once=True)
                else:
                    urls.extend(self.generate_urls(target, False))

            self.delay()

        for url in urls:
            self.collect(self.trim(url))

        self.loot()
