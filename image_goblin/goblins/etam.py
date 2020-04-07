from goblins.generic_gamma import GammaGoblin


class EtamGoblin(GammaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.modifiers = ('_x', '_a', '_b', '_c', '_d', '_6')
        self.img_pat = r'\d+_[a-z\d]\.jpg'
        self.iter = r'_[a-z\d]'
        self.url_base = 'https://www.etam.com/on/demandware.static/-/Sites-ELIN-master/default/'

    def __str__(self):
        return 'etam goblin'

    def __repr__(self):
        return 'etam'
