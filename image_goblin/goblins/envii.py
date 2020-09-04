from goblins.generic_gamma import GammaGoblin

# NOTE: can work with web too but url needs query string

class EnviiGoblin(GammaGoblin):

    NAME = 'envii goblin'
    ID = 'envii'
    MODIFIERS = [f'-{n}.jpg' if n > 1 else '.jpg' for n in range(1, 10)]
    IMG_PAT = r'[A-Z]\d+-\d+(-\d)?\.jpg'
    ITER_PAT = r'-?\d?\.jpg'
    URL_BASE = 'https://www.envii.com/on/demandware.static/-/Sites-envii-master-catalogue/default/images/images/hi-res/'
    QUERY = ''

    def __init__(self, args):
        super().__init__(args)
