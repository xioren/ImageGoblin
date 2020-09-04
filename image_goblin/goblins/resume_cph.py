from goblins.generic_alpha import AlphaGoblin


class ResumeGoblin(AlphaGoblin):

    ACCEPT_IMAGE = True
    ACCEPT_WEBPAGE = True

    NAME = 'resume goblin'
    ID = 'resume'

    def __init__(self, args):
        super().__init__(args)

    def generate_urls(self, url, image=True):
        if image:
            return [f'{url[:-5]}1.jpg']
        else:
            return self.parser.extract_by_regex(self.get(url).content, self.URL_PAT)
