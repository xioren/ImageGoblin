from goblins.generic_gamma import GammaGoblin

# NOTE: also uses https://images.calzedonia.com/get/w/500/h/750/IMAGE_ITER.jpg

class TezenisGoblin(GammaGoblin):

	NAME = 'tezenis goblin'
	ID = 'tezenis'
	MODIFIERS = ('FI', 'BI', 'M', 'DT1', 'C', 'B', 'F')
	IMG_PAT = r'(?<=/)\w+(_wear)?\w+_[A-Z\d]{,3}\.jpg'
	ITER_PAT = r'(?<=_)[A-Z\d]{,3}(?=\.)'
	URL_BASE = 'https://www.tezenis.com/dw/image/v2/BCXQ_PRD/on/demandware.static/-/Sites-TEZ_EC_COM/default/images/'
	QUERY = '?sw=3000&sfrm=png'

	def __init__(self, args):
		super().__init__(args)
