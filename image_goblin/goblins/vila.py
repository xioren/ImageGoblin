from goblins.generic_gamma import GammaGoblin


class VilaGoblin(GammaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.modifiers = ('_001', '_002', '_003', '_004', '_005', '_006', '_007', '_008', '_009')
        self.img_pat = r'\w+ProductLarge\.jpg'
        self.iter = r'_00\d'
        self.url_base = 'https://www.vila.com/on/demandware.static/-/Sites-pim-catalog/default/pim-static/large/'

    def __str__(self):
        return 'vila goblin'

    def __repr__(self):
        return 'vila'

    def generate_modifiers(self, iter):
        pass
