from goblins.generic_theta import ThetaGoblin


class ElseGoblin(ThetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'else goblin'

    def __repr__(self):
        return 'else'
