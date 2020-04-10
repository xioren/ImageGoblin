from goblins.generic_beta import BetaGoblin


class CalvinKleinGoblin(BetaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.accept_webpage = True
        self.query = '?fmt=jpeg&qlt=100&scl=1.4'
        self.modifiers = ('_main', '_alternate1', '_alternate2', '_alternate3', '_alternate4', 'alternate5')

    def __str__(self):
        return 'calvin klein goblin'

    def __repr__(self):
        return 'calvinklein'
