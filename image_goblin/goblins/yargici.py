from goblins.generic_epsilon import EpsilonGoblin


class YargiciGoblin(EpsilonGoblin):

    NAME = 'yargici goblin'
    ID = 'yargici'
    MOD_PAT = r'\d{8}'
    URL_END = '_0.jpeg'
    URL_PAT = r'https://img-incommerce-yargici\.mncdn[^"\s]+\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def generate_modifiers(self, url):
        id = int(self.parser.safe_search(self.MOD_PAT, url))
        self.modifiers = [i for i in range(id - 7, id + 7)]
