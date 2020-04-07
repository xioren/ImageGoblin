from goblins.shopify import ShopifyGoblin


class FashionNovaGoblin(ShopifyGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'fashion nova goblin'

    def __repr__(self):
        return 'fashionnova'