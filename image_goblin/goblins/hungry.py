from goblins.meta_goblin import MetaGoblin


class HungryGoblin(MetaGoblin):

    def __init__(self):
        self.meal = set()
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'hungry goblin'

    def __repr__(self):
        return 'hungry'

    def run(self):
        while True:
            bite = (input(f'[{self.__str__()}] <feed me> '))
            if bite == '':
                break
            self.meal.add(bite)
        return self.meal
