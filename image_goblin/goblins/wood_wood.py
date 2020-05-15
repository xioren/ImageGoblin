import re

from goblins.meta import MetaGoblin


class WoodWoodGoblin(MetaGoblin):
    '''accepts:
        - image
    '''

    NAME = 'wood wood goblin'
    ID = 'woodwood'
    # URL_PAT = r'https?://www\.woodwood\.com/shared/[^"\s]+\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        '''extract image id from url'''
        return re.search(r'/\d+/\d+/', url).group().strip('/').split('/')

    def upscale(self, url):
        '''sub in higher resolution cropping and return filename'''
        return re.sub(r'\d+x\d+c', '1600x2400c', self.parser.extract_filename(url))

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'shared' in target:
                urls = [target]
            else:
                urls = []
                self.logger.log(2, self.NAME, 'WARNING', 'webpage urls not supported', once=True)
            for url in urls:
                id, image_num = self.extract_id(url)
                filename = self.upscale(url)
                for n in range(int(image_num) - 6, int(image_num) + 7):
                    self.collect(f'https://www.woodwood.com/shared/{id}/{n}/{filename}.jpg',
                                 filename=filename.replace('1600x2400c', f'{id}-{n}'))
        self.loot()
