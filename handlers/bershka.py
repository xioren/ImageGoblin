from handlers.generic_delta import DeltaGoblin


class BershkaGoblin(DeltaGoblin):

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        self.size = 1
        print(f'[{self.__str__()}] <running>')

    def __str__(self):
        return 'bershka goblin'
