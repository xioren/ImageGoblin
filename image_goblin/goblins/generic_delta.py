import re

from goblins.meta import MetaGoblin


class DeltaGoblin(MetaGoblin):
    '''handles: Inditex Group (_n_n_n)
    accepts:
        - image
        - webpage*
    generic backend for:
        - bershka
        - massimodutti
        - oysho
        - pull&bear
        - stradivarius
        - zara
    '''

    URL_PAT = r'https?://static[^"]+_\d_\d_\d\.jpe?g'
    MODIFIERS = ('_1_1_', '_2_1_', '_2_2_', '_2_3_',
                 '_2_4_', '_2_5_', '_2_6_', '_2_7_',
                 '_2_8_', '_2_9_', '_4_1_', '_6_1_')

    def __init__(self, args):
        super().__init__(args)

    def trim(self, url):
        '''remove cropping from query string'''
        return re.sub(r'&imwidth=\d+', '', url)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'static' in target:
                urls = [target]
            else:
                if not self.ACCEPT_WEBPAGE:
                    urls = []
                    self.logger.log(2, self.NAME, 'WARNING', 'webpage urls not supported', once=True)
                else:
                    urls = self.extract_by_regex(self.URL_PAT, target)
            for url in urls:
                url_base, url_end = re.split(r'_\d_\d_\d+', url)
                for mod in self.MODIFIERS:
                    self.collect('{}{}{}{}'.format(re.sub(r"w/\d+/", "", url_base), mod, self.SIZE, self.trim(url_end)))
        self.loot()
