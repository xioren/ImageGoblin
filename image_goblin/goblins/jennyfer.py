from goblins.generic_gamma import GammaGoblin


class JennyferGoblin(GammaGoblin):

    NAME = 'jennyfer goblin'
    ID = 'jennyfer'
    MODIFIERS = ('_81', '_82', '_83', '_84')
    IMG_PAT = r'\w+_\d+_[A-Z]\.jpg'
    ITER_PAT = r'_\d+'
    URL_BASE = 'https://www.jennyfer.com/on/demandware.static/-/Sites-jennyfer-catalog-master/default/images/'

    def __init__(self, args):
        super().__init__(args)
