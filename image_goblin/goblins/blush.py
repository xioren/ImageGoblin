from goblins.generic_alpha import AlphaGoblin


# TODO: check if scanning possible


class BlushGoblin(AlphaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'blush goblin'

    def __repr__(self):
        return 'blush'
