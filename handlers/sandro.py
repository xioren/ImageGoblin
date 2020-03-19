from handlers.generic_gamma import GammaGoblin


class SandroGoblin(GammaGoblin):

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        self.modifiers = ('1', '2', '3', '4', '5', '6', '7', '8')
        self.pattern = r'Sandro_[A-Z0-9]+\-\d+_V_'
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'sandro goblin'
