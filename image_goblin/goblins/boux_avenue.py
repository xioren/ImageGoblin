from goblins.generic_gamma import GammaGoblin

# NOTE: can work with web too but url needs query string

class BouxAvenueGoblin(GammaGoblin):

    def __init__(self, args):
        super().__init__(args)
        # QUESTION: are there more than 3?
        self.modifiers = ('FR', 'BK', 'ST')
        self.img_pat = r'(?<=/)\d+_[A-Z\d]+_0_[A-Z]+\.jpg'
        self.iter_pat = r'[A-Z]+(?=\.)'
        self.url_base = 'https://www.bouxavenue.com/on/demandware.static/-/' \
                        'Sites-bouxavenue-master-catalog/default/'

    def __str__(self):
        return 'boux avenue goblin'

    def __repr__(self):
        return 'bouxavenue'
