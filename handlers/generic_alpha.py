import re
import os
from time import sleep
from handlers.meta_goblin import MetaGoblin


class AlphaGoblin(MetaGoblin):

    '''
    for: media/catalog variants
    accepts:
        - webpage
    generic back-end for:
        - agent provocateur
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
            # QUESTION: possible?
            pass
        else:
            parsed_links = re.finditer(self.image_pat, self.get_html(self.args['url']))
            for parsed in {p.group() for p in parsed_links}:
                self.loot(re.sub(r'cache/(\d/\w+/(\d+x(\d+)*/)*)*\w+/', '', parsed.replace('\\', '')), clean=self.clean)
                sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
