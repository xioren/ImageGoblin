from handlers.shopify import ShopifyGoblin


class CecilieGoblin(ShopifyGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'cecilie copenhagen goblin'
