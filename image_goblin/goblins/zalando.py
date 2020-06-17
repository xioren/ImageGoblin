from goblins.meta import MetaGoblin


# NOTE: video format: https://mosaic04.ztat.net.vgs.content/08/12/1C/0I/6Q/11/VIDEO/HIGH_QUALITY/1572009797216.mp4


class ZalandoGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'zalando goblin'
    ID = 'zalando'
    ID_PAT = r'[A-Z\d]+-[A-Z\d]{3}(?![\-\w])'

    def __init__(self, args):
        super().__init__(args)

    def form_url(self, filename):
        '''form url from filename'''
        compounded = f'{filename[:2]}/{filename[2:4]}/{filename[4:6]}/{filename[6:8]}/' \
                     f'{filename[8]}{filename[10]}/{filename[11:13]}/{filename}'

        return f'https://mosaic01.ztat.net/vgs/media/original/{compounded}.jpg'

    def extract_id(self, url):
        '''extract image id from url'''
        return self.parser.safe_search(self.ID_PAT, self.parser.extract_filename(url).upper())

    def run(self):
        self.toggle_collecton_type()
        self.logger.log(1, self.NAME, 'collecting urls')

        for target in self.args['targets'][self.ID]:
            self.new_collection()
            self.looted.clear()

            id = self.extract_id(target)
            if not id:
                continue

            for n in range(1, 51):
                self.collect(self.form_url(f'{id}@{n}'))

            self.loot(timeout=12)
