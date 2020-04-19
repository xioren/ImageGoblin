class Logger:
    '''Program Output'''

    def __init__(self, verbose, silent):
        self.verbose = verbose
        self.silent = silent

    def log(self, level, caller, msg, info=''):
        if level == 0: # basic output
            print(f'[{caller}] <{msg}> {info}')
        elif level == 1: # normal output
            if not self.silent:
                print(f'[{caller}] <{msg}> {info}')
        elif level == 2: # exceptions
            if self.verbose and not self.silent:
                print(f'[{caller}] <{msg}> {info}')
