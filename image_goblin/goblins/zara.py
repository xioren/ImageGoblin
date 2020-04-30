from goblins.generic_delta import DeltaGoblin


class ZaraGoblin(DeltaGoblin):

    NAME = 'zara goblin'
    ID = 'zara'
    SIZE = 0
    ACCEPT_WEBPAGE = True

    def __init__(self, args):
        super().__init__(args)
