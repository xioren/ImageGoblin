from goblins.generic_delta import DeltaGoblin


class PullandBearGoblin(DeltaGoblin):

    NAME = 'pull&bear goblin'
    ID = 'pullandbear'
    SIZE = 8
    API_URL = 'https://www.pullandbear.com/itxrest/2/catalog/store/24009477/20309419/category/0/product/{}/detail'
    URL_BASE = 'https://static.pullandbear.net/2/photos'
    MODIFIERS = [f'_{j}_{k}_' for j in range(1, 5) for k in range(1, 11)]

    def __init__(self, args):
        super().__init__(args)
