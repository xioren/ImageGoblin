from goblins.generic_gamma import GammaGoblin


class EtamGoblin(GammaGoblin):

    NAME = 'etam goblin'
    ID = 'etam'
    MODIFIERS = ('_x', '_a', '_b', '_c', '_d', '_6')
    IMG_PAT = r'\d+_[a-z\d]\.jpg'
    ITER_PAT = r'_[a-z\d](?=\.jpg)'
    URL_BASE = 'https://www.etam.com/on/demandware.static/-/Sites-ELIN-master/default/'
    QUERY = ''

    def __init__(self, args):
        super().__init__(args)
