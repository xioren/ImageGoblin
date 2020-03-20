import os
from time import sleep
from handlers.meta_goblin import MetaGoblin
from parsing import *


class IteratorGoblin(MetaGoblin):

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        self.increment = increment
        self.timeout = timeout
        self.idle = 0
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'iterator goblin'

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
        base, iterable, end = extract_iterable(self.url)
        iteration = 1
        print(f'[{self.__str__()}] <iterating> {self.url}')
        while True:
            url = f'{base}{iterable}{end}'
            if self.timed_out(self.timeout):
                self.cleanup(self.path_main)
                print(f'[{self.__str__()}] <timeout> after {self.timeout} attempts')
                return None
            if iteration % 25 == 0:
                print(f'[{self.__str__()}] <iteration> #{iteration}')
            attempt = self.loot(url)
            if attempt:
                self.idle = 0
            else:
                self.idle += 1
            iterable = str(int(iterable.lstrip('0')) + self.increment).zfill(len(iterable))
            iteration += 1
            sleep(self.tickrate)

    def run(self):
        self.iterate()
