from handlers.shopify import ShopifyGoblin


class FleurDuMalGoblin(ShopifyGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'fleur du mal goblin'