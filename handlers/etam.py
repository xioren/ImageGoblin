from handlers.generic_gamma import GammaGoblin


class EtamGoblin(GammaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.modifiers = ('_x', '_a', '_b', '_c', '_d', '_6')
        self.pattern = r'\d+_[a-z\d]\.jpg'
        self.iter = r'_[a-z\d]'
        self.base = 'https://www.etam.com/on/demandware.static/-/Sites-ELIN-master/default/'

    def __str__(self):
        return 'etam goblin'

    def generate_modifiers(self, iter):
        pass
