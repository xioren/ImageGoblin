from goblins.generic_alpha import AlphaGoblin

# BUG: server returning redirect error

class MaisonCloseGoblin(AlphaGoblin):

    NAME = 'maison close goblin'
    ID = 'maisonclose'
    ACCEPT_IMAGE = True
    ACCEPT_WEBPAGE = True

    def __init__(self, args):
        super().__init__(args)

    def generate_urls(self, url, image=True):
        if image:
            return [self.parser.regex_sub(r'_\d_', f'_{n}_', url) for n in range(1, 10)]
        else:
            # NOTE: usually throws redirect loop error
            return self.parser.extract_by_regex(self.get(url).content, self.URL_PAT)
