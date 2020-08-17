from goblins.generic_epsilon import EpsilonGoblin


class KotonGoblin(EpsilonGoblin):

	NAME = 'koton goblin'
	ID = 'koton'
	MOD_PAT = r'G\d+_zoom\d'
	URL_END = '_V01.jpg'
	URL_PAT = r'https?://ktnimg\.mncdn[^"\s]+zoom\d_V01\.jpg'

	def __init__(self, args):
		super().__init__(args)

	def generate_modifiers(self, url):
		self.modifiers = [f'G0{n}_zoom{n}' for n in range(1, 8)]
