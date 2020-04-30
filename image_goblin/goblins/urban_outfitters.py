from goblins.generic_beta import BetaGoblin


class UrbanOutfittersGoblin(BetaGoblin):

    NAME = 'urban outfitters goblin'
    ID = 'urbanoutfitters'
    ACCEPT_WEBPAGE = True
    MODIFIERS = ('_a', '_b', '_c', '_d', '_e', '_f', '_g', '_h', '_0')

    def __init__(self, args):
        super().__init__(args)
