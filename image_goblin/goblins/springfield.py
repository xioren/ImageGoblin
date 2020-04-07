from goblins.generic_gamma import GammaGoblin


class SpringfieldGoblin(GammaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.modifiers = ('FM', 'TM', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8')
        self.img_pat = r'P_[A-Z\d]+\.jpg'
        self.iter = r'[A-Z][A-Z\d]'
        self.url_base = 'https://myspringfield.com/on/demandware.static/-/Sites-gc-spf-master-catalog/default/images/hi-res/'

    def __str__(self):
        return 'springfield goblin'

    def __repr__(self):
        return 'springfield'