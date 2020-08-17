from goblins.generic_delta import DeltaGoblin


class StradivariusGoblin(DeltaGoblin):

	NAME = 'stradivarius goblin'
	ID = 'stradivarius'
	SIZE = 1
	API_URL = 'https://www.stradivarius.com/itxrest/2/catalog/store/54109556/50331080/category/0/product/{}/detail'
	URL_BASE = 'https://static.e-stradivarius.net/5/photos3'
	MODIFIERS = [f'_{j}_{k}_' for j in range(1, 11) for k in range(1, 5)]

	def __init__(self, args):
		super().__init__(args)

	def extract_urls(self, url):
		'''extract urls from html'''
		return self.parser.extract_by_regex(self.get(url).content, self.URL_PAT)
