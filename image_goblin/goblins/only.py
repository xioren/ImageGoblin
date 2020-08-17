from goblins.generic_gamma import GammaGoblin


class OnlyGoblin(GammaGoblin):

	NAME = 'only goblin'
	ID = 'only'
	MODIFIERS = [f'_00{n}' for n in range(1, 10)]
	IMG_PAT = r'\w+ProductLarge\.jpg'
	ITER_PAT = r'_00\d'
	URL_BASE = 'https://www.only.com/on/demandware.static/-/Sites-pim-catalog/default/pim-static/large/'
	QUERY = ''

	def __init__(self, args):
		super().__init__(args)
