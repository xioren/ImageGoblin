from goblins.shopify import ShopifyGoblin


class HanneBlochGoblin(ShopifyGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'hanne bloch goblin'

    def __repr__(self):
        return 'hannebloch'