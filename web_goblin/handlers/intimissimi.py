import re
from handlers.generic_zeta import ZetaGoblin


class IntimissimiGoblin(ZetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'intimissimi goblin'

    def __repr__(self):
        return 'intimissimi'
