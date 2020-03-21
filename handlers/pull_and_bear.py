from handlers.generic_delta import DeltaGoblin


class PullandBearGoblin(DeltaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.size = 8

    def __str__(self):
        return 'pull&bear goblin'
