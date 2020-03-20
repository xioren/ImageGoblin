import os
from time import sleep
from handlers.meta_goblin import MetaGoblin


class IteratorGoblin(MetaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.idle = 0

    def __str__(self):
        return 'iterator goblin'

    def extract_iterable(self, url):
        '''
        seperate iterable from a url (mode 3)
        '''
        return re.split('%%%', url)

    def timed_out(self, n):
        '''
        program idle tracking
        '''
        if n > 0 and self.idle >= n:
            return True
        else:
            return False

    def iterate(self):
        '''
        re-forms url and iterates (mode 3)
        '''
        base, iterable, end = self.extract_iterable(self.args['url'])
        iteration = 1
        print(f'[{self.__str__()}] <iterating> {self.args["url"]}')
        while True:
            url = f'{base}{iterable}{end}'
            if self.timed_out(self.args['timeout']):
                self.cleanup(self.path_main)
                print(f'[{self.__str__()}] <timeout> after {self.args["timeout"]} attempts')
                return None
            if iteration % 25 == 0:
                print(f'[{self.__str__()}] <iteration> #{iteration}')
            attempt = self.loot(url)
            if attempt:
                self.idle = 0
            else:
                self.idle += 1
            iterable = str(int(iterable.lstrip('0')) + self.args['increment']).zfill(len(iterable))
            iteration += 1
            sleep(self.args['tickrate'])

    def run(self):
        self.iterate()
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
