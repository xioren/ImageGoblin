from handlers.generic_gamma import GammaGoblin

# NOTE: can work with web too but url needs query string

class BouxAvenueGoblin(GammaGoblin):

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        self.modifiers = ('FR', 'BK', 'ST')
        self.pattern = r'\d+_[A-Z0-9]+_0_'
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'boux avenue goblin'
