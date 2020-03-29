import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class DeltaGoblin(MetaGoblin):

    '''
    handles: Inditex Group (_n_n_n)
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
        self.ids = ('_1_1_', '_2_1_', '_2_2_', '_2_3_',
                    '_2_4_', '_2_5_', '_2_6_', '_2_7_',
                    '_2_8_', '_2_9_', '_4_1_', '_6_1_')

    def clean(self, url):
        return re.sub(r'&imwidth=\d+', '', url)

    def run(self):
        if '.jpg' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(r'https*://static[^"]+\.jpe*g', self.args['url'])
        for link in links:
            base, end = re.split(r'_\d_\d_\d+', link)
            for id in self.ids:
                self.collect(self.decrop(f'{base}{id}{self.size}{self.clean(end)}'))
        self.loot()
