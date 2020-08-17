from goblins.generic_theta import ThetaGoblin


class UnderprotectionGoblin(ThetaGoblin):

	NAME = 'underprotection goblin'
	ID = 'underprotection'

	def __init__(self, args):
		super().__init__(args)
