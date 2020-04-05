from goblins.generic_beta import BetaGoblin


class AnthropologieGoblin(BetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'anthropologie goblin'

    def __repr__(self):
        return 'anthropologie'

    def identify(self, url):
        self.modifiers = ('_b', '_b2', '_b3', '_b4', '_b4', '_c', '_c2', '_c3', '_c4', '_c5')
        return 'https://s7d5.scene7.com/is/image/Anthropologie/'
