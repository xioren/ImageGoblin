from goblins.generic_iota import IotaGoblin


class AnthropologieGoblin(IotaGoblin):

    NAME = 'anthropologie goblin'
    ID = 'anthropologie'
    MODIFIERS = [f'_{m}{n}' if n > 1 else f'_{m}' for n in range(1, 6) for m in ('b', 'c')]
    API_URL = 'https://www.anthropologie.com/api/catalog/v0/an-us/pools/US_DIRECT/products?slug={}&projection-slug=pdp'
    AUTH_API_URL = 'https://www.anthropologie.com/slipstream/api/token/v0/an-us/auth'

    def __init__(self, args):
        super().__init__(args)
