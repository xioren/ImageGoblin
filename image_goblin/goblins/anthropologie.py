from goblins.generic_iota import IotaGoblin


class AnthropologieGoblin(IotaGoblin):

    NAME = 'anthropologie goblin'
    ID = 'anthropologie'
    MODIFIERS = ('_b', '_b2', '_b3', '_b4', '_b4', '_c', '_c2', '_c3', '_c4', '_c5')
    API_URL = 'https://www.anthropologie.com/api/catalog/v0/an-us/pools/US_DIRECT/products?slug={}&projection-slug=pdp'
    AUTH_API_URL = 'https://www.anthropologie.com/slipstream/api/token/v0/an-us/auth'

    def __init__(self, args):
        super().__init__(args)
