from goblins.generic_theta import ThetaGoblin


class UnderprotectionGoblin(ThetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'underprotection goblin'

    def __repr__(self):
        return 'underprotection'
