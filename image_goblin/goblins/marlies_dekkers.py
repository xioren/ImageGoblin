from goblins.generic_gamma import GammaGoblin


class MarliesDekkersGoblin(GammaGoblin):

    def __init__(self, args):
        super().__init__(args)
        # QUESTION: are there more than 3?
        self.modifiers = ('1_lb_f', '2_lb_f', '3_lb_b', '4_lb_b')
        self.img_pat = r'\d+_\d_lb_\w+\.jpg'
        self.iter_pat = r'\d_lb_[bf]'
        self.url_base = 'https://www.marliesdekkers.com/on/demandware.static/-/Sites-Master/default/'

    def __str__(self):
        return 'marlies dekkers goblin'

    def __repr__(self):
        return 'marliesdekkers'
