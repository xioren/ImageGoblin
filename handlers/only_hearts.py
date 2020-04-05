from handlers.generic_alpha import AlphaGoblin


class OnlyHeartsGoblin(AlphaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'only hearts goblin'

    def __repr__(self):
        return 'onlyhearts'
