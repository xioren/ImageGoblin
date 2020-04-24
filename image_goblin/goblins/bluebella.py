from goblins.generic_theta import ThetaGoblin


class BlueBellaGoblin(ThetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'bluebella goblin'

    def __repr__(self):
        return 'bluebella'
