from goblins.generic_delta import DeltaGoblin


class PullandBearGoblin(DeltaGoblin):

    NAME = 'pull&bear goblin'
    ID = 'pullandbear'
    ACCEPT_WEBPAGE = False
    SIZE = 8

    def __init__(self, args):
        super().__init__(args)
