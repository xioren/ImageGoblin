from goblins.generic_theta import ThetaGoblin


class ShopifyGoblin(ThetaGoblin):

    NAME = 'shopify goblin'
    ID = 'shopify'

    def __init__(self, args):
        super().__init__(args)
