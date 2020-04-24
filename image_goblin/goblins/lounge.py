from goblins.generic_theta import ThetaGoblin


class LoungeGoblin(ThetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'lounge goblin'

    def __repr__(self):
        return 'lounge'
