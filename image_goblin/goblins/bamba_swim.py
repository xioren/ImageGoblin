from goblins.shopify import ShopifyGoblin


class BambaSwimGoblin(ShopifyGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'bamba swim goblin'
