from goblins.generic_delta import DeltaGoblin


class OyshoGoblin(DeltaGoblin):

    NAME = 'oysho goblin'
    ID = 'oysho'
    SIZE = 0
    API_URL = 'https://www.oysho.com/itxrest/2/catalog/store/64009613/60361120/category/0/product/{}/detail'
    URL_BASE = 'https://static.oysho.net/6/photos2'
    MODIFIERS = [f'_{j}_{k}_' for j in range(1, 21) for k in range(1, 10)]

    def __init__(self, args):
        super().__init__(args)
