from handlers.generic_beta import BetaGoblin


class TommyHilfigerGoblin(BetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'tommy hilfiger goblin'

    def identify(self, link):
        if 'tommy-europe' in link:
            self.chars = ('main', 'alternate1', 'alternate2', 'alternate3', 'alternate4')
            return 'https://tommy-europe.scene7.com/is/image/TommyEurope/'
        else:
            self.chars = ('FNT', 'BCK', 'DE1', 'DE2', 'DE3')
            return 'https://shoptommy.scene7.com/is/image/ShopTommy/'
