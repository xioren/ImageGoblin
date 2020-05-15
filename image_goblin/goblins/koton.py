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
        self.modifiers = ('G01_zoom1', 'G02_zoom2', 'G03_zoom3', 'G04_zoom4',
                          'G05_zoom5', 'G06_zoom6', 'G07_zoom7')
