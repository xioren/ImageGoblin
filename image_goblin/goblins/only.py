from goblins.generic_gamma import GammaGoblin


class OnlyGoblin(GammaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.modifiers = ('_001', '_002', '_003', '_004', '_005', '_006', '_007', '_008', '_009')
        self.img_pat = r'\w+ProductLarge\.jpg'
        self.iter_pat = r'_00\d'
        self.url_base = 'https://www.only.com/on/demandware.static/-/Sites-pim-catalog/default/pim-static/large/'

    def __str__(self):
        return 'only goblin'

    def __repr__(self):
        return 'only'
