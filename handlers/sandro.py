from handlers.generic_gamma import GammaGoblin


class SandroGoblin(GammaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.modifiers = ('1', '2', '3', '4', '5', '6', '7', '8')
        self.pattern = r'Sandro_[A-Z0-9]+\-\d+_V_'
        self.base = 'https://us.sandro-paris.com/on/demandware.static/-/Sites-sandro-catalog-master-H13/default/images/h13/'

    def __str__(self):
        return 'sandro goblin'
