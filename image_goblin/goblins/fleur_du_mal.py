from goblins.generic_theta import ThetaGoblin


class FleurDuMalGoblin(ThetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'fleur du mal goblin'

    def __repr__(self):
        return 'fleurdumal'
