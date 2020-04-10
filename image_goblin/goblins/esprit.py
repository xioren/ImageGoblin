from goblins.generic_beta import BetaGoblin


class EspritGoblin(BetaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.accept_webpage = True
        self.modifiers = [f'_{n}' for n in range(10, 20)]

    def __str__(self):
        return 'esprit goblin'

    def __repr__(self):
        return 'esprit'
