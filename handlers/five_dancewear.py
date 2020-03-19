from handlers.shopify import ShopifyGoblin


class FiveDancewearGoblin(ShopifyGoblin):

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'five dancwear goblin'
