from goblins.generic_beta import BetaGoblin


class FreePeopleGoblin(BetaGoblin):

    NAME = 'free people goblin'
    ID = 'freepeople'
    ACCEPT_WEBPAGE = True
    MODIFIERS = ('_a', '_b', '_c', '_d', '_e')

    def __init__(self, args):
        super().__init__(args)
