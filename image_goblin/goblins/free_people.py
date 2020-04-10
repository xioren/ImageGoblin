from goblins.generic_beta import BetaGoblin


class FreePeopleGoblin(BetaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.accept_webpage = True
        self.modifiers = ('_a', '_b', '_c', '_d', '_e')

    def __str__(self):
        return 'free people goblin'

    def __repr__(self):
        return 'freepeople'
