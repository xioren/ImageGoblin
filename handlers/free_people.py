from handlers.generic_beta import BetaGoblin


class FreePeopleGoblin(BetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'free people goblin'

    def identify(self, link):
        self.modifiers = ('a', 'b', 'c', 'd', 'e')
        return 'https://s7d5.scene7.com/is/image/FreePeople/'
