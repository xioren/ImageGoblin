from goblins.generic_delta import DeltaGoblin

# QUESTION: remove everything after initial query?

class MassimoDuttiGoblin(DeltaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.size = 0
        self.accept_webpage = True

    def __str__(self):
        return 'massimo dutti goblin'

    def __repr__(self):
        return 'massimodutti'
