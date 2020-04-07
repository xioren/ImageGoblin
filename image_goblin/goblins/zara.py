from goblins.generic_delta import DeltaGoblin


class ZaraGoblin(DeltaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.size = 0
        self.accept_webpage = True

    def __str__(self):
        return 'zara goblin'

    def __repr__(self):
        return 'zara'
