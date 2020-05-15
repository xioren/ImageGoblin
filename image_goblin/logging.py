from math import floor
from os import get_terminal_size

class Logger:
    '''Program Output'''

    def __init__(self, verbose, silent):
        self.verbose = verbose
        self.silent = silent
        self.logged = [] # keep track of log once logs

    def log(self, level, caller, msg, info='', clear=False, once=False):
        '''logging messages
        - level 0: basic
        - level 1: normal
        - level 2: verbose
        '''
        if clear:
            try:
                print(' ' * get_terminal_size().columns, end='\r')
            except OSError: # ioctl error when redirecting output, such as to a text file.
                pass
        if level == 1 and self.silent:
            pass
        elif level == 2 and not self.verbose or self.silent:
            pass
        else:
            output = f'[{caller}] <{msg}> {info}'
            if output not in self.logged:
                print(output)
                if once:
                    self.logged.append(output)

    def progress(self, caller, msg, current, total):
        '''progress bar'''
        if not self.verbose and not self.silent:
            bar =  '#' * floor(current/total * 20)
            # QUESTION: add clear here?
            print(f'[{caller}] <{msg}> [{bar.ljust(20, " ")}] {current} of {total}', end='\r')
