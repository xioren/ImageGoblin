import re
from handlers.meta_goblin import MetaGoblin


class AlphaGoblin(MetaGoblin):

    '''
    for: media/catalog variants
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
        self.clean=True
        self.image_pat = r'https*\:[^" \n]+media[^" \n]+\.jpe*g'

    def run(self):
        if '.jpg' in self.args['url']:
            links = []
            if not self.args['silent']:
                print(f'[{self.__str__()}] <WARNING> url type not supported')
        else:
            links = self.extract_links(self.image_pat, self.args['url'])
        for link in links:
            self.collect(re.sub(r'cache/(\d/\w+/(\d+x(\d+)*/)*)*\w+/', '', link.replace('\\', '')), clean=self.clean)
        self.loot()
