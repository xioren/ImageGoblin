from goblins.generic_eta import EtaGoblin


class NastyGalGoblin(EtaGoblin):

    NAME = 'nasty gal goblin'
    ID = 'nastygal'
    URL_PAT = r'media\.nastygal\.com/i/[a-z]+/[\w_]+'

    def __init__(self, args):
        super().__init__(args)
