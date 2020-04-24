from goblins.generic_theta import ThetaGoblin


class VitaminAGoblin(ThetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'vitamin a goblin'

    def __repr__(self):
        return 'vitamina'
