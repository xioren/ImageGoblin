from goblins.generic_beta import BetaGoblin


class EspritGoblin(BetaGoblin):

    NAME = 'esprit goblin'
    ID = 'esprit'
    ACCEPT_WEBPAGE = True
    MODIFIERS = [f'_{n}' for n in range(10, 20)]

    def __init__(self, args):
        super().__init__(args)
