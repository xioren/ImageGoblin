from goblins.generic_eta import EtaGoblin


class BoohooGoblin(EtaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'boohoo goblin'

    def __repr__(self):
        return 'boohoo'
