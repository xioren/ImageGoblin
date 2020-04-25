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
        self.id_pat = re.compile(r'[A-Z0-9]+-[A-Z0-9]{3}(?![\-\w])')

    def __str__(self):
        return 'zalando goblin'

    def __repr__(self):
        return 'zalando'

    def form_url(self, filename):
        '''form url from filename'''
        compounded = f'{filename[:2]}/{filename[2:4]}/{filename[4:6]}/{filename[6:8]}/' \
                     f'{filename[8]}{filename[10]}/{filename[11:13]}/{filename}'
        return f'https://mosaic01.ztat.net/vgs/media/original/{compounded}.jpg'

    def extract_id(self, url):
        '''extract image id from url'''
        return re.search(self.id_pat, self.parser.extract_filename(url).upper()).group()

    def run(self):
        self.toggle_collecton_type()
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            self.new_collection()
            id = self.extract_id(target)
            for n in range(1, 50):
                self.collect(self.form_url(f'{id}@{n}'))
            self.loot(timeout=8)
