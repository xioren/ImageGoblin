from handlers.generic_beta import BetaGoblin


class EspritGoblin(BetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'esprit goblin'

    def identify(self, link):
        self.modifiers = [f'_{n}' for n in range(10, 20)]
        return 'https://esprit.scene7.com/is/image/esprit/'
