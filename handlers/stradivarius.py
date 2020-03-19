from handlers.generic_delta import DeltaGoblin


class StradivariusGoblin(DeltaGoblin):

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        self.size = 1
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'stradivarius goblin'
