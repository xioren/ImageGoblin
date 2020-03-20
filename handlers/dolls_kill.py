import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class DollsKillGoblin(MetaGoblin):

    '''
    accepts:
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'dolls kill goblin'

    def run(self):
        html = self.get_html(self.args['url'])
        for link in {l.group() for l in re.finditer(r'img src="https://media.dollskill.com[^"]+\-\d+.jpg', html)}:
            self.loot(re.sub(r'\d+.jpg', '1.jpeg', link).replace('img src="', ''))
            sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
