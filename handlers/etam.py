from handlers.generic_gamma import GammaGoblin


class EtamGoblin(GammaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.modifiers = ('x', 'a', 'b', 'c', 'd', '6')
        self.pattern = r'\d+_'
        self.base = 'https://www.etam.com/on/demandware.static/-/Sites-ELIN-master/default/'

    def __str__(self):
        return 'etam goblin'
