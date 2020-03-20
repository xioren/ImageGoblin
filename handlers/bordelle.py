from handlers.shopify import ShopifyGoblin


class BordelleGoblin(ShopifyGoblin):

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        self.clean = False
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'bordelle goblin'
