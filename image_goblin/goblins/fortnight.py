from goblins.generic_theta import ThetaGoblin


class FortnightGoblin(ThetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'fortnight goblin'

    def __repr__(self):
        return 'fortnight'
