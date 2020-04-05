from goblins.shopify import ShopifyGoblin


class KikiDeMontparnasseGoblin(ShopifyGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'kiki de montparnasse goblin'

    def __repr__(self):
        return 'kikidemontparnasse'
