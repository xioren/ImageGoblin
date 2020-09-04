from goblins.generic_alpha import AlphaGoblin


class BrabooGoblin(AlphaGoblin):

    NAME = 'braboo goblin'
    ID = 'braboo'
    ACCEPT_IMAGE = False
    ACCEPT_WEBPAGE = True

    def __init__(self, args):
        super().__init__(args)

    def generate_urls(self, url, image=True):
        if image:
            return [f'{url[:-5]}{n}.jpg' for n in range(1, 6)]
        else:
            return self.parser.extract_by_regex(self.get(url).content, self.URL_PAT)
