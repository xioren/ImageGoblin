from goblins.generic_theta import ThetaGoblin


class TrianglGoblin(ThetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'triangl goblin'

    def __repr__(self):
        return 'triangl'
