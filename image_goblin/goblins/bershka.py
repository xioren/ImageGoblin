from goblins.generic_delta import DeltaGoblin


class BershkaGoblin(DeltaGoblin):

    NAME = 'bershka goblin'
    ID = 'bershka'
    SIZE = 0
    API_URL = 'https://www.bershka.com/itxrest/2/catalog/store/45009578/40259530/category/0/product/{}/detail'
    URL_BASE = 'https://static.bershka.net/4/photos2'
    MODIFIERS = [f'_{j}_{k}_' for j in range(1, 8) for k in range(1, 11)]

    def __init__(self, args):
        super().__init__(args)
