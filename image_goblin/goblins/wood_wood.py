import re

from goblins.meta import MetaGoblin


class WoodWoodGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
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
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'shared' in target:
                urls.append(target)
            else:
                self.headers.update({'Cookie': 'queue=1589683924; bbc=104.149.68.66'})
                urls.extend(self.parser.extract_by_regex(self.get(target).content, r'(?<="og:image" content=")[^"]+'))

        for url in urls:
            id, image_num = self.extract_id(url)
            filename = self.upscale(url)

            for n in range(int(image_num) - 6, int(image_num) + 7):
                self.collect(f'https://www.woodwood.com/shared/{id}/{n}/{filename}.jpg',
                             filename=filename.replace('1600x2400c', f'{id}-{n}'))

        self.loot()
