from time import sleep
from handlers.meta_goblin import MetaGoblin


class TopshopGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    url types:
        - image
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, tickrate, verbose, nodl)
        self.mode = mode
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'topshop goblin'

    def run(self):
        link = dequerry(self.url)[:-5]
        for n in range(1, 6):
            self.loot(f'{url}{n}.jpg')
            sleep(self.tickrate)
