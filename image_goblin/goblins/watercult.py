import re

from goblins.generic_alpha import AlphaGoblin


class WatercultGoblin(AlphaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.accept_image = True
        self.accept_webpage = True

    def __str__(self):
        return 'watercult goblin'

    def __repr__(self):
        return 'watercult'

    def generate_urls(self, url, image=True):
        if image:
            url_base = re.sub(r'-\d(_\d)?\.jpg', '', url)
            return [f'{url_base}-{n}.jpg' for n in (1, 2, 3, 9)]
        else:
            return self.extract_by_regex(self.url_pat, url)
