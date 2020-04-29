from goblins.generic_theta import ThetaGoblin


class ShopifyGoblin(ThetaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'shopify goblin'

    def __repr__(self):
        return 'shopify'
