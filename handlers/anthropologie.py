from handlers.generic_beta import BetaGoblin


class AnthropologieGoblin(BetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'anthropologie goblin'

    def identify(self, link):
        self.modifiers = ('b', 'b2', 'b3', 'b4', 'b4', 'c', 'c2', 'c3', 'c4', 'c5')
        return 'https://s7d5.scene7.com/is/image/Anthropologie/'
