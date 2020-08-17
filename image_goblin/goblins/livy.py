from goblins.generic_gamma import GammaGoblin


class LivyGoblin(GammaGoblin):

	NAME = 'livy goblin'
	ID = 'livy'
	MODIFIERS = ('_x', '_a', '_b', '_c', '_d', '_6')
	IMG_PAT = r'\d+_[a-z\d]\.jpg'
	ITER_PAT = r'_[a-z\d]'
	URL_BASE = 'https://www.li-vy.com/on/demandware.static/-/Sites-LLIN-master/default/'
	QUERY = ''

	def __init__(self, args):
		super().__init__(args)
