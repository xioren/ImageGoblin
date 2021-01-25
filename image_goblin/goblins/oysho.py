from goblins.generic_delta import DeltaGoblin


class OyshoGoblin(DeltaGoblin):

    NAME = 'oysho goblin'
    ID = 'oysho'
    SIZE = 0
    API_URL = 'https://www.oysho.com/itxrest/2/catalog/store/64009613/60361120/category/0/product/{}/detail'
    URL_BASE = 'https://static.oysho.net/6/photos2'
    # MODIFIERS = [f'_{j}_{k}_' for j in range(1, 21) for k in range(1, 10)]
    MODIFIERS = ['_1_1_', '_2_1_', '_2_2_', '_2_3_', '_2_4_', '_2_5_', '_2_6_',
                 '_2_7_', '_2_8_', '_2_9_', '_1_7_', '_6_1_', '_7_1_', '_12_1_']

    def __init__(self, args):
        super().__init__(args)
