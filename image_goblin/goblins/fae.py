from goblins.shopify import ShopifyGoblin


class FaeGoblin(ShopifyGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'fae goblin'

    def __repr__(self):
        return 'fae'
