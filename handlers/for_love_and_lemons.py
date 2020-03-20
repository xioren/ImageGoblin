from handlers.shopify import ShopifyGoblin


class ForLoveAndLemonsGoblin(ShopifyGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'for love and lemons goblin'
