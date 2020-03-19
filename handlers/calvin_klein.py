from handlers.generic_beta import BetaGoblin


class CalvinKleinGoblin(BetaGoblin):

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'calvin klein goblin'

    def identify(self, link):
        self.chars = ('main', 'alternate1', 'alternate2', 'alternate3', 'alternate4', 'alternate5')
        if 'CalvinKleinEU' in link:
            return 'https://calvinklein-eu.scene7.com/is/image/CalvinKleinEU/',  '?&wid=2750'
        else:
            return 'https://calvinklein.scene7.com/is/image/CalvinKlein/', '?&wid=1510'
