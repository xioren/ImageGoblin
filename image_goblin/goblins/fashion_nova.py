from goblins.generic_theta import ThetaGoblin


class FashionNovaGoblin(ThetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'fashion nova goblin'

    def __repr__(self):
        return 'fashionnova'
