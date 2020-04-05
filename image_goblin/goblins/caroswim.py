from goblins.shopify import ShopifyGoblin


class CaroSwimGoblin(ShopifyGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'caro swim goblin'

    def __repr__(self):
        return 'caroswim'
