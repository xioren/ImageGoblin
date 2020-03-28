import os
import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class IteratorGoblin(MetaGoblin):

    '''
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'iterator goblin'

    def extract_iterable(self, url):
        '''
        seperate iterable from a url (mode 3)
        '''
        return re.split('%%%', url)

    # IDEA: instead of hard coding 100, maybe use double timeout value.
    def extend_iterable(self, iterable):
        extended = []
        for _ in range(100):
            extended.append(iterable)
            iterable = str(int(iterable.lstrip('0')) + self.args['increment']).zfill(len(iterable))
        return extended

    def increment_iterable(self, iterable):
        return str(int(iterable.lstrip('0')) + 100).zfill(len(iterable))

    def iterate(self):
        '''
        re-forms url and iterates (mode 3)
        '''
        round = 1
        base, iterable, end = self.extract_iterable(self.args['url'])
        while True:
            # OPTIMIZE: make such that re-instatiation is not needed
            self.sorted_collection = []
            print(f'[{self.__str__()}] <iterating> round {round}')
            for iter in self.extend_iterable(iterable):
                self.collect(f'{base}{iter}{end}', sorted=True)
            attempt = self.loot(timeout=self.args['timeout'])
            if attempt:
                round += 1
                iterable = self.increment_iterable(iterable)
            else:
                print(f'[{self.__str__()}] <timeout> after {self.args["timeout"]} attempts')
                return None

    def run(self):
        self.iterate()
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
