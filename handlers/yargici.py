import re
from handlers.generic_epsilon import EpsilonGoblin


class YargiciGoblin(EpsilonGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.mod_pat = r'\d{8}'
        self.end = '_0.jpeg'
        self.img_pat = r'https://img-incommerce-yargici\.mncdn[^" ]+\.jpg'

    def __str__(self):
        return 'yargici goblin'

    def custom(self, url):
        return url.replace('Thumbs', 'Originals')

    def generate_ids(self, url):
        id = int(re.search(self.mod_pat, url).group())
        self.modifiers = [i for i in range(id - 7, id + 7)]
