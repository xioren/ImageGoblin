from handlers.shopify import ShopifyGoblin


class TheGreatErosGoblin(ShopifyGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'the great eros goblin'

    def __repr__(self):
        return 'thegreateros'
