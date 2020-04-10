from goblins.generic_beta import BetaGoblin


class AnthropologieGoblin(BetaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.accept_webpage = True
        self.modifiers = ('_b', '_b2', '_b3', '_b4', '_b4', '_c', '_c2', '_c3', '_c4', '_c5')

    def __str__(self):
        return 'anthropologie goblin'

    def __repr__(self):
        return 'anthropologie'
