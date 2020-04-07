from goblins.generic_beta import BetaGoblin


class UrbanOutfittersGoblin(BetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'urban outfitters goblin'

    def __repr__(self):
        return 'urbanoutfitters'

    def identify(self, url):
        self.modifiers = ('_a', '_b', '_c', '_d', '_e', '_f', '_g', '_h', '_0')
        if 'UrbanOutfittersEU' in url:
            return 'https://s7g10.scene7.com/is/image/UrbanOutfittersEU/'
        else:
            return 'https://s7d5.scene7.com/is/image/UrbanOutfitters/'