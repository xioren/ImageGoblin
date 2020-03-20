from handlers.generic_gamma import GammaGoblin


class WomensSecretGoblin(GammaGoblin):

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        self.modifiers = ('FM', 'TM', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8')
        self.pattern = r'P_\d+'
        self.base = 'https://womensecret.com/on/demandware.static/-/Sites-gc-ws-master-catalog/default/images/hi-res/'
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'womens secret goblin'
