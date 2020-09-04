from goblins.generic_epsilon import EpsilonGoblin


class LcWaikikiGoblin(EpsilonGoblin):

    NAME = 'lc waikiki goblin'
    ID = 'lcwaikiki'
    MOD_PAT = r'_[a-z]?\d?(?=\.jpg)'
    URL_END = '.jpg'
    URL_PAT = r'https://img-lcwaikiki.mncdn.com([\w\-/]+)?/productimages/[^\.]+\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def generate_modifiers(self, url):
        self.modifiers = [f'_{m}{n}' if n > 0 else f'_{m}' for n in range(4) for m in ('a', 'b')]
