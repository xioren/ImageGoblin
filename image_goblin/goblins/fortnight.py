from goblins.shopify import ShopifyGoblin


class FortnightGoblin(ShopifyGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'fortnight goblin'

    def __repr__(self):
        return 'fortnight'
