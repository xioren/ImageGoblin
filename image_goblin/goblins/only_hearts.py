from goblins.generic_alpha import AlphaGoblin


class OnlyHeartsGoblin(AlphaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.accept_image = False
        self.accept_webpage = True

    def __str__(self):
        return 'only hearts goblin'

    def __repr__(self):
        return 'onlyhearts'

    def generate_urls(self, url, image=True):
        if image:
            return [url]
        else:
            return self.extract_urls_greedy(self.url_pat, url)
