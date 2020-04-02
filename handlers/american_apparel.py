from handlers.generic_beta import BetaGoblin


class AmericanApparelGoblin(BetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'american apparel goblin'

    def identify(self, link):
        self.modifiers = ('', '_01', '_02', '_03', '_04', '_05')
        return 'https://s7d9.scene7.com/is/image/AmericanApparel/'
