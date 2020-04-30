from goblins.generic_delta import DeltaGoblin


class OyshoGoblin(DeltaGoblin):

    NAME = 'oysho goblin'
    ID = 'oysho'
    ACCEPT_WEBPAGE = False
    SIZE = 0

    def __init__(self, args):
        super().__init__(args)
