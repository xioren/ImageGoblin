from goblins.generic_beta import BetaGoblin


class CalvinKleinGoblin(BetaGoblin):

    NAME = 'calvin klein goblin'
    ID = 'calvinklein'
    ACCEPT_WEBPAGE = True
    QUERY = '?fmt=jpeg&qlt=100&scl=1.4'
    MODIFIERS = ('_main', '_alternate1', '_alternate2', '_alternate3',
                 '_alternate4', 'alternate5')

    def __init__(self, args):
        super().__init__(args)
