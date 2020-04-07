import re

from goblins.generic_epsilon import EpsilonGoblin


class YargiciGoblin(EpsilonGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.mod_pat = r'\d{8}'
        self.url_end = '_0.jpeg'
        self.url_pat = r'https://img-incommerce-yargici\.mncdn[^" ]+\.jpg'

    def __str__(self):
        return 'yargici goblin'

    def __repr__(self):
        return 'yargici'

    def generate_modifiers(self, url):
        id = int(re.search(self.mod_pat, url).group())
        self.modifiers = [i for i in range(id - 7, id + 7)]
