from goblins.shopify import ShopifyGoblin


class UnderprotectionGoblin(ShopifyGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'underprotection goblin'

    def __repr__(self):
        return 'underprotection'
