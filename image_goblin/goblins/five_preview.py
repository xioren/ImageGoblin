from goblins.generic_alpha import AlphaGoblin


class FivePreviewGoblin(AlphaGoblin):

	ACCEPT_IMAGE = True
	ACCEPT_WEBPAGE = True

	NAME = '5preview goblin'
	ID = '5preview'

	def __init__(self, args):
		super().__init__(args)

	def generate_urls(self, url, image=True):
		if image:
			return [f'{url[:-5]}{n}.jpg'for n in ('a', 'b')]
		else:
			return self.parser.extract_by_regex(self.get(url).content, self.URL_PAT)
