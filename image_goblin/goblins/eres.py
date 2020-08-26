from goblins.generic_gamma import GammaGoblin


class EresGoblin(GammaGoblin):

	NAME = 'eres goblin'
	ID = 'eres'
	MODIFIERS = [n for n in range(1, 6)]
	IMG_PAT = r'\d+_\d+_PDP_[A-Z]_\d\.jpg'
	ITER_PAT = r'\d(?=\.)'
	URL_BASE = 'https://www.eresparis.com/on/demandware.static/-/Sites-master/default/images/lingerie/PDP_D/'
	QUERY = ''

	def __init__(self, args):
		super().__init__(args)
