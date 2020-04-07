from goblins.generic_delta import DeltaGoblin


class OyshoGoblin(DeltaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.size = 0
        self.accept_webpage = False

    def __str__(self):
        return 'oysho goblin'

    def __repr__(self):
        return 'oysho'
