from handlers.meta_goblin import MetaGoblin


class Goblin(MetaGoblin):

    '''
    mode options:
        -
    accepts:
        -
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return ' goblin'

    def run(self):
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
