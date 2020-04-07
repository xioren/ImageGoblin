from goblins.generic_delta import DeltaGoblin


class BershkaGoblin(DeltaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.size = 1
        self.accept_webpage = False

    def __str__(self):
        return 'bershka goblin'

    def __repr__(self):
        return 'bershka'
