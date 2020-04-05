from handlers.generic_delta import DeltaGoblin


class MassimoDuttiGoblin(DeltaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.size = 0

    def __str__(self):
        return 'massimo dutti goblin'

    def __repr__(self):
        return 'massimodutti'
