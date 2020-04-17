class Logger:
    '''Program Output'''

    def __init__(self, verbose, silent):
        self.verbose = verbose
        self.silent = silent

    def log(self, level, caller, err, msg=''):
        if level == 0:
            print(f'[{caller}] <{err}> {msg}')
        elif level == 1:
            if not self.silent:
                print(f'[{caller}] <{err}> {msg}')
        elif level == 2:
            if self.verbose and not self.silent:
                print(f'[{caller}] <{err}> {msg}')
