from handlers.shopify import ShopifyGoblin


class TrianglGoblin(ShopifyGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'triangl goblin'