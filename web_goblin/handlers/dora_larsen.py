from handlers.shopify import ShopifyGoblin


class DoraLarsenGoblin(ShopifyGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'dora larsen goblin'

    def __repr__(self):
        return 'doralarsen'
