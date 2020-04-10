from goblins.generic_beta import BetaGoblin


class TommyHilfigerGoblin(BetaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.accept_webpage = False

    def __str__(self):
        return 'tommy hilfiger goblin'

    def __repr__(self):
        return 'tommyhilfiger'

    @property
    def modifiers(self):
        if 'europe' in self.url_base:
            return ('_main', '_alternate1', '_alternate2', '_alternate3', '_alternate4')
        else:
            return ('_FNT', '_BCK', '_DE1', '_DE2', '_DE3')
