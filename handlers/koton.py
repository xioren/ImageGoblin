from handlers.generic_epsilon import EpsilonGoblin


class KotonGoblin(EpsilonGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.ids = ('G01_zoom1', 'G02_zoom2', 'G03_zoom3', 'G04_zoom4', 'G05_zoom5', 'G06_zoom6', 'G07_zoom7')
        self.id_pat = r'G\d+_zoom\d'
        self.img_pat = r'https://ktnimg\.mncdn[^" ]+zoom\d_V01\.jpg'

    def __str__(self):
        return 'koton goblin'

    def custom(self, url):
        return url.replace('zoom1', 'zoom2')
