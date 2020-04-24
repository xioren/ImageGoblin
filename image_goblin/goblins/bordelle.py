from goblins.generic_theta import ThetaGoblin


class BordelleGoblin(ThetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'bordelle goblin'

    def __repr__(self):
        return 'bordelle'
