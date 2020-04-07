from goblins.generic_alpha import AlphaGoblin


class BikiniLoversGoblin(AlphaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.accept_image = False
        self.accept_webpage = True

    def __str__(self):
        return 'bikini lovers goblin'

    def __repr__(self):
        return 'bikinilovers'

    def generate_urls(self, url, image=True):
        if image:
            pass
        else:
            return self.extract_urls(self.url_pat, url)
