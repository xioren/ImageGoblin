from handlers.generic_gamma import GammaGoblin


class JennyferGoblin(GammaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.modifiers = (81, 82, 83, 84)
        self.pattern = r'\d+_\d+_[A-Z].jpg'
        self.iter = r'_\d+'
        self.base = 'https://www.jennyfer.com/on/demandware.static/-/Sites-jennyfer-catalog-master/default/images/'

    def __str__(self):
        return 'jennyfer goblin'

    def __repr__(self):
        return 'jennyfer'

    def generate_modifiers(self, iter):
        pass
