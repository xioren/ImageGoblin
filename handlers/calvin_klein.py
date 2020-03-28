from handlers.generic_beta import BetaGoblin


class CalvinKleinGoblin(BetaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.query = '?fmt=jpeg&qlt=100&scl=1.3'

    def __str__(self):
        return 'calvin klein goblin'

    def identify(self, link):
        self.chars = ('main', 'alternate1', 'alternate2', 'alternate3', 'alternate4', 'alternate5')
        if 'CalvinKleinEU' in link:
            return 'https://calvinklein-eu.scene7.com/is/image/CalvinKleinEU/'
        else:
            return 'https://calvinklein.scene7.com/is/image/CalvinKlein/'
