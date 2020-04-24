from goblins.generic_eta import EtaGoblin

class NastyGalGoblin(EtaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'media\.nastygal\.com/i/[a-z]+/[\w_]+'


    def __str__(self):
        return 'nasty gal goblin'

    def __repr__(self):
        return 'nastygal'
