from handlers.generic_alpha import AlphaGoblin


class BikiniLoversGoblin(AlphaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'bikini lovers goblin'

    def __repr__(self):
        return 'bikinilovers'
