from goblins.generic_theta import ThetaGoblin


class SkinGoblin(ThetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'skin goblin'

    def __repr__(self):
        return 'skin'
