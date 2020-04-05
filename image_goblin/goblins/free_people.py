from goblins.generic_beta import BetaGoblin


class FreePeopleGoblin(BetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'free people goblin'

    def __repr__(self):
        return 'freepeople'

    def identify(self, url):
        self.modifiers = ('_a', '_b', '_c', '_d', '_e')
        return 'https://s7d5.scene7.com/is/image/FreePeople/'
