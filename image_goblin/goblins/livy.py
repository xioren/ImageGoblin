from goblins.generic_gamma import GammaGoblin


class LivyGoblin(GammaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.modifiers = ('_x', '_a', '_b', '_c', '_d', '_6')
        self.img_pat = r'\d+_[a-z\d]\.jpg'
        self.iter_pat = r'_[a-z\d]'
        self.url_base = 'https://www.li-vy.com/on/demandware.static/-/Sites-LLIN-master/default/'

    def __str__(self):
        return 'livy goblin'

    def __repr__(self):
        return 'livy'

    def generate_modifiers(self, iter):
        pass
