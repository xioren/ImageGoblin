import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class YandyGoblin(MetaGoblin):

    '''
    accepts:
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'yandy goblin'

    def run(self):
        html = self.get_html(self.args['url'])
        for link in {l.group() for l in re.finditer(r'https://assets.yandycdn.com/Products/[^-]+-\d+.jpg', html)}:
            self.loot(link.replace('Products', 'HiRez'))
            sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
