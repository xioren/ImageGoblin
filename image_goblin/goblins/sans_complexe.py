from goblins.generic_alpha import AlphaGoblin


class SansComplexeGoblin(AlphaGoblin):

    NAME = 'sans complexe goblin'
    ID = 'sanscomplexe'
    ACCEPT_IMAGE = True
    ACCEPT_WEBPAGE = True

    def __init__(self, args):
        super().__init__(args)

    def generate_urls(self, url, image=True):
        if image:
            url_base = self.parser.regex_sub(r'\d\.jpg', '', url)
            return [f'{url_base}{n}.jpg' for n in range(1, 7)]
        else:
            return self.parser.extract_by_regex(self.get(url).content, self.URL_PAT)
