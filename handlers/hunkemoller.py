import re
from handlers.generic_gamma import GammaGoblin

# NOTE: https://images-hunkemoller.akamaized.net/original/

class HunkemollerGoblin(GammaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.modifiers = ('1', '2', '3', '4', '5')
        self.pattern = r'\d+_'
        self.base = 'https://www.hunkemoller.co.uk/on/demandware.static/-/Sites-hkm-master/default/images/large/'

    def __str__(self):
        return 'hunkemoller goblin'
