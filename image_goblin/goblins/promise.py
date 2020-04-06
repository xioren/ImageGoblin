from goblins.generic_alpha import AlphaGoblin


class PromiseGoblin(AlphaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'promise goblin'

    def __repr__(self):
        return 'promise'
