from goblins.meta import MetaGoblin


class HungryGoblin(MetaGoblin):

    NAME = 'hungry goblin'

    def __init__(self):
        self.meal = set()
        print(f'[{self.NAME}] <deployed>')

    def run(self):
        while True:
            bite = input(f'[{self.NAME}] <feed me> ')
            if bite == '':
                break
            self.meal.add(bite)
        return self.meal
