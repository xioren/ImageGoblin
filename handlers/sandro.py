from handlers.generic_gamma import GammaGoblin


class SandroGoblin(GammaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.modifiers = ('V_1', 'V_2', 'V_3', 'V_4', 'V_5', 'V_6', 'V_7', 'V_8')
        self.img_pat = r'Sandro_[A-Z\d]+\-\d+_V_\d\.jpg'
        self.iter = r'V_\d'
        self.url_base = 'https://us.sandro-paris.com/on/demandware.static/-/Sites-sandro-catalog-master-H13/default/images/h13/'

    def __str__(self):
        return 'sandro goblin'

    def generate_modifiers(self, iter):
        pass
