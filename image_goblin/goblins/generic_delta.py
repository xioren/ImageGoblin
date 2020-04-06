import re
from time import sleep
from goblins.meta import MetaGoblin


class DeltaGoblin(MetaGoblin):
    '''handles: Inditex Group (_n_n_n)
    accepts:
        - image
        - webpage
    generic backend for:
        - bershka
        - massimodutti
        - oysho
        - pull&bear
        - stradivarius
        - zara
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'https*://static[^"]+\.jpe*g'
        self.modifiers = ('_1_1_', '_2_1_', '_2_2_', '_2_3_',
                          '_2_4_', '_2_5_', '_2_6_', '_2_7_',
                          '_2_8_', '_2_9_', '_4_1_', '_6_1_')

    def decrop(self, url):
        return re.sub(r'&imwidth=\d+', '', url)

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if '.jpg' in target:
                urls = [target]
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                base, end = re.split(r'_\d_\d_\d+', url)
                for mod in self.modifiers:
                    self.collect(self.decrop(f'{base}{mod}{self.size}{self.decrop(end)}'))
        self.loot()
