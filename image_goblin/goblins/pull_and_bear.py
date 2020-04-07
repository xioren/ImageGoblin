from goblins.generic_delta import DeltaGoblin


class PullandBearGoblin(DeltaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.size = 8
        self.accept_webpage = False

    def __str__(self):
        return 'pull&bear goblin'

    def __repr__(self):
        return 'pullandbear'
