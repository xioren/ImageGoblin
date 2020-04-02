from handlers.generic_beta import BetaGoblin


class TommyHilfigerGoblin(BetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'tommy hilfiger goblin'

    def identify(self, link):
        if 'tommy-europe' in link:
            self.modifiers = ('_main', '_alternate1', '_alternate2', '_alternate3', '_alternate4')
            return 'https://tommy-europe.scene7.com/is/image/TommyEurope/'
        else:
            self.modifiers = ('_FNT', '_BCK', '_DE1', '_DE2', '_DE3')
            return 'https://shoptommy.scene7.com/is/image/ShopTommy/'
