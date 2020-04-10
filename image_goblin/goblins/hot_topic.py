from goblins.generic_beta import BetaGoblin


class HotTopicGoblin(BetaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.accept_webpage = True
        self.modifiers = ('_hi', '_av1', '_av2', '_av3')

    def __str__(self):
        return 'hot topic goblin'

    def __repr__(self):
        return 'hottopic'
