from handlers.meta_goblin import MetaGoblin


class HungryGoblin(MetaGoblin):

    '''
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'hungry goblin'

    def run(self):
        while True:
            food = input(f'[{self.__str__()}] <feed me> ')
            if food == '':
                break
            if self.args['format']:
                food = self.user_format(food)
            self.collect(food)
        self.loot()
