from goblins.generic_delta import DeltaGoblin


class BershkaGoblin(DeltaGoblin):

    NAME = 'bershka goblin'
    ID = 'bershka'
    SIZE = 1
    ACCEPT_WEBPAGE = False

    def __init__(self, args):
        super().__init__(args)
