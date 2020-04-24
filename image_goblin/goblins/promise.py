from goblins.generic_alpha import AlphaGoblin


class PromiseGoblin(AlphaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.accept_image = False
        self.accept_webpage = True

    def __str__(self):
        return 'promise goblin'

    def __repr__(self):
        return 'promise'

    def generate_urls(self, url, image=True):
        if image:
            return [url]
        else:
            return self.extract_by_regex(self.url_pat, url)
