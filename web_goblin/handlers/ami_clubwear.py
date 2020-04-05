from handlers.generic_alpha import AlphaGoblin


class AMIGoblin(AlphaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'ami clubwear goblin'

    def __repr__(self):
        return 'amiclubwear'
