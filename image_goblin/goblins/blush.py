from goblins.generic_alpha import AlphaGoblin


# TODO: check if scanning possible


class BlushGoblin(AlphaGoblin):

    ACCEPT_IMAGE = True
    ACCEPT_WEBPAGE = True

    NAME = 'blush goblin'
    ID = 'blush'

    def __init__(self, args):
        super().__init__(args)

    def generate_urls(self, url, image=True):
        if image:
            return [f'{url[:-5]}{n}.jpg'for n in range(1, 10)]
        else:
            return self.parser.extract_by_regex(self.get(url).content, self.URL_PAT)
