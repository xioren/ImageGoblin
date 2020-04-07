from goblins.generic_epsilon import EpsilonGoblin


class KotonGoblin(EpsilonGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.mod_pat = r'G\d+_zoom\d'
        self.url_end = '_V01.jpg'
        self.url_pat = r'https://ktnimg\.mncdn[^" ]+zoom\d_V01\.jpg'

    def __str__(self):
        return 'koton goblin'

    def __repr__(self):
        return 'koton'

    def generate_modifiers(self, url):
        self.modifiers = ('G01_zoom1', 'G02_zoom2', 'G03_zoom3', 'G04_zoom4', 'G05_zoom5', 'G06_zoom6', 'G07_zoom7')
