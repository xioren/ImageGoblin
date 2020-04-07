import re

from goblins.generic_gamma import GammaGoblin


# legacy: https://images-hunkemoller.akamaized.net/original/


class HunkemollerGoblin(GammaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.modifiers = ('_1', '_2', '_3', '_4', '_5')
        self.iter = r'_\d'
        self.img_pat = r'\d+_\d\.jpg'
        self.url_base = 'https://www.hunkemoller.co.uk/on/demandware.static/-/Sites-hkm-master/default/images/large/'

    def __str__(self):
        return 'hunkemoller goblin'

    def __repr__(self):
        return 'hunkemoller'
