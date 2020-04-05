from goblins.shopify import ShopifyGoblin


class ElseGoblin(ShopifyGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'else goblin'

    def __repr__(self):
        return 'else'
