from goblins.generic_delta import DeltaGoblin


class StradivariusGoblin(DeltaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.size = 1

    def __str__(self):
        return 'stradivarius goblin'

    def __repr__(self):
        return 'stradivarius'
