from math import floor
from os import get_terminal_size

class Logger:
    '''Program Output'''

    def __init__(self, verbose, silent):
        self.verbose = verbose
        self.silent = silent

    def log(self, level, caller, msg, info='', clear=False):
        '''logging messages'''
        if clear:
            print(' ' * get_terminal_size().columns, end='\r')
        if level == 0: # basic output
            print(f'[{caller}] <{msg}> {info}')
        elif level == 1: # normal output
            if not self.silent:
                print(f'[{caller}] <{msg}> {info}')
        elif level == 2: # verbose output
            if self.verbose and not self.silent:
                print(f'[{caller}] <{msg}> {info}')

    def progress(self, caller, msg, current, total):
        '''progress bar'''
        if not self.verbose and not self.silent:
            bar =  '#' * floor(current/total * 20)
            print(f'[{caller}] <{msg}> [{bar.ljust(20, " ")}] {current} of {total}', end='\r')
