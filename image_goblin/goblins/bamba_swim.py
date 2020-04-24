from goblins.generic_theta import ThetaGoblin


class BambaSwimGoblin(ThetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'bamba swim goblin'

    def __repr__(self):
        return 'bambaswim'
