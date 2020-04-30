from goblins.generic_delta import DeltaGoblin

# QUESTION: remove everything after initial query?

class MassimoDuttiGoblin(DeltaGoblin):

    NAME = 'massimo dutti goblin'
    ID = 'massimodutti'
    ACCEPT_WEBPAGE = True
    SIZE = 0

    def __init__(self, args):
        super().__init__(args)
