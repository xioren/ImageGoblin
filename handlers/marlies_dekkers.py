from handlers.generic_gamma import GammaGoblin


class MarliesDekkersGoblin(GammaGoblin):

    def __init__(self, args):
        super().__init__(args)
        # QUESTION: are there more than 3?
        self.modifiers = ('1_lb_f', '2_lb_f', '3_lb_b', '4_lb_b')
        self.pattern = r'\d+_\d_lb_\w+\.jpg'
        self.iter = r'\d_lb_[bf]'
        self.base = 'https://www.marliesdekkers.com/on/demandware.static/-/Sites-Master/default/'

    def __str__(self):
        return 'marlies dekkers goblin'

    def generate_modifiers(self, iter):
        pass
