from handlers.generic_beta import BetaGoblin


class UrbanOutfittersGoblin(BetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'urban outfitters goblin'

    def identify(self, link):
        self.chars = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', '0')
        if 'UrbanOutfittersEU' in link:
            return 'https://s7g10.scene7.com/is/image/UrbanOutfittersEU/'
        else:
            return 'https://s7d5.scene7.com/is/image/UrbanOutfitters/'
