from handlers.generic_beta import BetaGoblin


class HotTopicGoblin(BetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'hot topic goblin'

    def identify(self, link):
        self.chars = ('hi', 'av1', 'av2', 'av3')
        return 'https://hottopic.scene7.com/is/image/HotTopic/'
