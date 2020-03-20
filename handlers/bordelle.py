from handlers.shopify import ShopifyGoblin


class BordelleGoblin(ShopifyGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.clean = False

    def __str__(self):
        return 'bordelle goblin'
