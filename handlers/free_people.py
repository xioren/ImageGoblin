from handlers.generic_beta import BetaGoblin


class FreePeopleGoblin(BetaGoblin):

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        print(f'[{self.__str__()}] <running>')

    def __str__(self):
        return 'free people goblin'

    def identify(self, link):
        self.chars = ('a', 'b', 'c', 'd', 'e')
        return 'https://s7d5.scene7.com/is/image/FreePeople/', '?wid=2640'
