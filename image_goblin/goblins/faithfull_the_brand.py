from goblins.shopify import ShopifyGoblin


class FaithfullTheBrandGoblin(ShopifyGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'faithfull the brand goblin'

    def __repr__(self):
        return 'faithfullthebrand'