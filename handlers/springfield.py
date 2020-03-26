from handlers.generic_gamma import GammaGoblin


class SpringfieldGoblin(GammaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.modifiers = ('FM', 'TM', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8')
        self.pattern = r'P_[A-Z\d]+\.jpg'
        self.iter = r'[A-Z][A-Z\d]'
        self.base = 'https://myspringfield.com/on/demandware.static/-/Sites-gc-spf-master-catalog/default/images/hi-res/'

    def __str__(self):
        return 'springfield goblin'

    def generate_modifiers(self, iter):
        pass
