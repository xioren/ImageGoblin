from goblins.generic_gamma import GammaGoblin


class MarliesDekkersGoblin(GammaGoblin):

    NAME = 'marlies dekkers goblin'
    ID = 'marliesdekkers'
    MODIFIERS = ('1_lb_f', '2_lb_f', '3_lb_b', '4_lb_b')
    IMG_PAT = r'\d+_\d_lb_\w+\.jpg'
    ITER_PAT = r'\d_lb_[bf]'
    URL_BASE = 'https://www.marliesdekkers.com/on/demandware.static/-/Sites-Master/default/'
    QUERY = ''

    def __init__(self, args):
        super().__init__(args)
