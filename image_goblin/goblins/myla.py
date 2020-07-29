from goblins.generic_theta import ThetaGoblin


class MylaGoblin(ThetaGoblin):

    NAME = 'myla goblin'
    ID = 'myla'

    def __init__(self, args):
        super().__init__(args)
