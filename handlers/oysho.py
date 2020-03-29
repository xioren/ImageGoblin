from handlers.generic_delta import DeltaGoblin


class OyshoGoblin(DeltaGoblin):

    def __init__(self, args):
        super().__init__(args)
        if self.args['format']:
            self.size = self.args['format'][0]
        else:
            self.size = 0

    def __str__(self):
        return 'oysho goblin'
