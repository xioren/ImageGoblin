from logging import Logger


logger = Logger(False, False)


class HungryGoblin:

    NAME = 'hungry goblin'

    def __init__(self):
        self.meal = set()
        logger.log(0, self.NAME, 'deployed')

    def run(self):
        while True:
            bite = input(f'[{self.NAME}] <feed me> ')
            if bite == '':
                break
            self.meal.add(bite)

        logger.log(0, self.NAME, 'digesting')
        return self.meal
