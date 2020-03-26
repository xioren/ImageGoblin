import re
import os
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

    def upgrade(self, path, base):
        '''
        upgrade existing files
        '''
        # NOTE: unused
        base = base.rstrip('/')
        for file in os.listdir(path):
            file = re.sub(r'\.(jpe*g|png)', '', file)
            self.loot(f'{base}/media/catalog/product/{file[0]}/{file[1]}/{file}.jpg')
            sleep(self.args['tickrate'])

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
