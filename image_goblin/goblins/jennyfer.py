from goblins.generic_gamma import GammaGoblin


class JennyferGoblin(GammaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.modifiers = ('_81', '_82', '_83', '_84')
        self.img_pat = r'\w+_\d+_[A-Z]\.jpg'
        self.iter_pat = r'_\d+'
        self.url_base = 'https://www.jennyfer.com/on/demandware.static/-/Sites-jennyfer-catalog-master/default/images/'

    def __str__(self):
        return 'jennyfer goblin'

    def __repr__(self):
        return 'jennyfer'
