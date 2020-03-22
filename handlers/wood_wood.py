import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class WoodWoodGoblin(MetaGoblin):

    '''
    mode options:
        -
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'wood wood goblin'

    def extract_id(self, url):
        return re.search(r'/\d+/\d+/', url).group().strip('/').split('/')

    def extract_name(self, url):
        return re.sub(r'\d+x\d+c', '1600x2400c',re.search(r'[^ "/]+\.jpg$', url).group().replace('.jpg', ''))

    def run(self):
        if 'shared' in self.args['url']:
            links = [self.args['url']]
        else:
            # links = self.extract_links(r'https*://www\.woodwood\.com/shared/[^" ]+\.jpg', self.args['url'])
            links = []
            if not self.args['silent']:
                print(f'[{self.__str__()}] <WARNING> url type not supported')
        for link in links:
            id, image_num = self.extract_id(link)
            name = self.extract_name(link)
            for n in range(int(image_num) - 6, int(image_num) + 7):
                self.loot(f'https://www.woodwood.com/shared/{id}/{n}/{name}.jpg', filename=name.replace('1600x2400c', f'{id}-{n}'))
                sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
