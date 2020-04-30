import re

from goblins.generic_alpha import AlphaGoblin


class AMIGoblin(AlphaGoblin):

    NAME = 'ami clubwear goblin'
    ID = 'amiclubwear'
    ACCEPT_IMAGE = False
    ACCEPT_WEBPAGE = True

    def __init__(self, args):
        super().__init__(args)

    def generate_urls(self, url, image=True):
        if image:
            return [url]
        else:
            return self.extract_by_regex(self.URL_PAT, url)
