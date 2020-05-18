from goblins.generic_gamma import GammaGoblin


class VilaGoblin(GammaGoblin):

    NAME = 'vila goblin'
    ID = 'vila'
    MODIFIERS = ('_001', '_002', '_003', '_004', '_005', '_006', '_007', '_008', '_009')
    IMG_PAT = r'\w+ProductLarge\.jpg'
    ITER_PAT = r'_00\d'
    URL_BASE = 'https://www.vila.com/on/demandware.static/-/Sites-pim-catalog/default/pim-static/large/'
    QUERY = ''

    def __init__(self, args):
        super().__init__(args)
