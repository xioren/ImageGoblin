from handlers.shopify import ShopifyGoblin


class FiveDancewearGoblin(ShopifyGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'five dancwear goblin'
