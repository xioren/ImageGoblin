from goblins.generic_theta import ThetaGoblin


class KikiDeMontparnasseGoblin(ThetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'kiki de montparnasse goblin'

    def __repr__(self):
        return 'kikidemontparnasse'
