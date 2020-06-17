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
        self.modifiers = ('_a', '_a1', '_a2', '_a3',
                          '_b', '_b1', '_b2', '_b3')
