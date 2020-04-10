import re

from goblins.meta import MetaGoblin


# NOTE: video format: https://mosaic04.ztat.net.vgs.content/08/12/1C/0I/6Q/11/VIDEO/HIGH_QUALITY/1572009797216.mp4


class ZalandoGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.toggle_collecton_type()

    def __str__(self):
        return 'zalando goblin'

    def __repr__(self):
        return 'zalando'

    def form_url(self, image):
        '''form url from filename'''
        compounded = f'{image[:2]}/{image[2:4]}/{image[4:6]}/{image[6:8]}/'\
                     f'{image[8]}{image[10]}/{image[11:13]}/{image}'
        return f'https://mosaic01.ztat.net/vgs/media/original/{compounded}.jpg'

    def extract_id(self, url):
        '''extract image id from url'''
        return re.search(r'[A-Z0-9]+-[A-Z0-9]{3}(?![\-\w])', self.extract_filename(url).upper()).group()

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            self.new_collection()
            id = self.extract_id(target)
            for n in range(1, 50):
                self.collect(self.form_url(f'{id}@{n}'))
            self.loot(timeout=8)
