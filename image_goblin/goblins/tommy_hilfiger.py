from goblins.generic_beta import BetaGoblin


class TommyHilfigerGoblin(BetaGoblin):

	NAME = 'tommy hilfiger goblin'
	ID = 'tommyhilfiger'
	ACCEPT_WEBPAGE = True

	def __init__(self, args):
		super().__init__(args)

	@property
	def MODIFIERS(self):
		if 'europe' in self.url_base:
			return ('_main', '_alternate1', '_alternate2', '_alternate3', '_alternate4')
		else:
			return ('_FNT', '_BCK', '_DE1', '_DE2', '_DE3')
