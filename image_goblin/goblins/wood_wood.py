import re

from goblins.meta import MetaGoblin


class WoodWoodGoblin(MetaGoblin):
    '''accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https?://www\.woodwood\.com/shared/[^" ]+\.jpg'

    def __str__(self):
        return 'wood wood goblin'

    def __repr__(self):
        return 'woodwood'

    def extract_id(self, url):
        '''extract image id from url'''
        return re.search(r'/\d+/\d+/', url).group().strip('/').split('/')

    def upscale(self, url):
        '''sub in higher resolution cropping and return filename'''
        return re.sub(r'\d+x\d+c', '1600x2400c', self.parser.extract_filename(url))

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'shared' in target:
                urls = [target]
            else:
                urls = []
                self.logger.log(1, self.__str__(), 'WARNING', 'webpage urls not supported')
            for url in urls:
                id, image_num = self.extract_id(url)
                filename = self.upscale(url)
                for n in range(int(image_num) - 6, int(image_num) + 7):
                    self.collect(f'https://www.woodwood.com/shared/{id}/{n}/{filename}.jpg',
                                 filename=filename.replace('1600x2400c', f'{id}-{n}'))
        self.loot()
