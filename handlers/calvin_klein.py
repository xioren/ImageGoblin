from handlers.generic_beta import BetaGoblin


class CalvinKleinGoblin(BetaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.query = '?fmt=jpeg&qlt=100&scl=1.3'

    def __str__(self):
        return 'calvin klein goblin'

    def identify(self, link):
        self.modifiers = ('_main', '_alternate1', '_alternate2', '_alternate3', '_alternate4', 'alternate5')
        if 'CalvinKleinEU' in link:
            return 'https://calvinklein-eu.scene7.com/is/image/CalvinKleinEU/'
        else:
            return 'https://calvinklein.scene7.com/is/image/CalvinKlein/'
