from handlers.generic_gamma import GammaGoblin


class WomensSecretGoblin(GammaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.modifiers = ('FM', 'TM', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8')
        self.pattern = r'P_\d+'
        self.base = 'https://womensecret.com/on/demandware.static/-/Sites-gc-ws-master-catalog/default/images/hi-res/'

    def __str__(self):
        return 'womens secret goblin'