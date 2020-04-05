from goblins.shopify import ShopifyGoblin


class BordelleGoblin(ShopifyGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'bordelle goblin'
