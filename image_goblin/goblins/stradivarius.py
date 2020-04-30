from goblins.generic_delta import DeltaGoblin


class StradivariusGoblin(DeltaGoblin):

    NAME = 'stradivarius goblin'
    ID = 'stradivarius'
    ACCEPT_WEBPAGE = True
    SIZE = 1

    def __init__(self, args):
        super().__init__(args)
