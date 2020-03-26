from handlers.generic_gamma import GammaGoblin


class JennyferGoblin(GammaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.pattern = r'\d+_\d+_[A-Z].jpg'
        self.iter = r'_\d+'
        self.base = 'https://www.jennyfer.com/on/demandware.static/-/Sites-jennyfer-catalog-master/default/images/'

    def __str__(self):
        return 'jennyfer goblin'

    def generate_modifiers(self, iter):
        iter = int(iter.lstrip('_'))
        self.modifiers = [f'_{n}' for n in range(iter-5, iter+6)]
