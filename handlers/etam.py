from handlers.generic_gamma import GammaGoblin


class EtamGoblin(GammaGoblin):

    '''
    large: https://www.etam.es/on/demandware.static/-/Sites-ELIN-master/default/dw7925a901/
    small: https://www.etam.es/dw/image/v2/AAWW_PRD/on/demandware.static/-/Sites-ELIN-master/default/dw91d8a790/
    # NOTE: when expanding images (on website), some are lower quality; make sure to use the high quality ones (they take longer to load)
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        self.modifiers = ('x', 'a', 'b', 'c', 'd', '6')
        self.pattern = r'\d+_'
        self.base = 'https://www.etam.com/on/demandware.static/-/Sites-ELIN-master/default/'
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'etam goblin'
