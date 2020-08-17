from goblins.generic_gamma import GammaGoblin


class SpringfieldGoblin(GammaGoblin):

	NAME = 'springfield goblin'
	ID = 'springfield'
	MODIFIERS = ('FM', 'TM', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8')
	IMG_PAT = r'P_[A-Z\d]+\.jpg'
	ITER_PAT = r'[A-Z\d]{2}(?=\.)'
	URL_BASE = 'https://myspringfield.com/on/demandware.static/-/Sites-gc-spf-master-catalog/default/images/hi-res/'
	QUERY = ''

	def __init__(self, args):
		super().__init__(args)
