import re
from handlers.generic_gamma import GammaGoblin

# NOTE: https://images-hunkemoller.akamaized.net/original/

class HunkemollerGoblin(GammaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.modifiers = ('_1', '_2', '_3', '_4', '_5')
        self.pattern = r'\d+_\d\.jpg'
        self.iter = r'_\d'
        self.base = 'https://www.hunkemoller.co.uk/on/demandware.static/-/Sites-hkm-master/default/images/large/'

    def __str__(self):
        return 'hunkemoller goblin'

    def generate_modifiers(self, iter):
        pass
