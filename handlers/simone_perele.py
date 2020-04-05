from handlers.generic_alpha import AlphaGoblin


class SimonePereleGoblin(AlphaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.clean = False

    def __str__(self):
        return 'simone perele goblin'

    def __repr__(self):
        return 'simoneperele'
