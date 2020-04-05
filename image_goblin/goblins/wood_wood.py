import re
from goblins.meta import MetaGoblin


class WoodWoodGoblin(MetaGoblin):

    '''
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'wood wood goblin'

    def __repr__(self):
        return 'woodwood'

    def extract_id(self, url):
        return re.search(r'/\d+/\d+/', url).group().strip('/').split('/')

    def extract_name(self, url):
        return re.sub(r'\d+x\d+c', '1600x2400c',re.search(r'[^ "/]+\.jpg$', url).group().replace('.jpg', ''))

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'shared' in target:
                urls = [target]
            else:
                # urls = self.extract_urls(r'https*://www\.woodwood\.com/shared/[^" ]+\.jpg', self.args['url'])
                urls = []
                if not self.args['silent']:
                    print(f'[{self.__str__()}] <WARNING> url type not supported')
            for url in urls:
                id, image_num = self.extract_id(url)
                name = self.extract_name(url)
                for n in range(int(image_num) - 6, int(image_num) + 7):
                    self.collect(f'https://www.woodwood.com/shared/{id}/{n}/{name}.jpg', filename=name.replace('1600x2400c', f'{id}-{n}'))
        self.loot()
