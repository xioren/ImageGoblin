from goblins.generic_gamma import GammaGoblin


class SandroGoblin(GammaGoblin):

	NAME = 'sandro goblin'
	ID = 'sandro'
	MODIFIERS = [f'V_{n}' for n in range(1, 9)]
	IMG_PAT = r'Sandro_[A-Z\d]+-\d+_V_\d\.jpg'
	ITER_PAT = r'V_\d'
	URL_BASE = 'https://us.sandro-paris.com/on/demandware.static/-/Sites-sandro-catalog-master-H13/default/images/h13/'
	QUERY = ''

	def __init__(self, args):
		super().__init__(args)
