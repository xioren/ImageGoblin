from goblins.generic_beta import BetaGoblin


class HotTopicGoblin(BetaGoblin):

	NAME = 'hot topic goblin'
	ID = 'hottopic'
	ACCEPT_WEBPAGE = True
	MODIFIERS = ('_hi', '_av1', '_av2', '_av3')

	def __init__(self, args):
		super().__init__(args)
