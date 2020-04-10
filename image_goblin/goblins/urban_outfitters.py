from goblins.generic_beta import BetaGoblin


class UrbanOutfittersGoblin(BetaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.accept_webpage = True
        self.modifiers = ('_a', '_b', '_c', '_d', '_e', '_f', '_g', '_h', '_0')

    def __str__(self):
        return 'urban outfitters goblin'

    def __repr__(self):
        return 'urbanoutfitters'
