import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class PrettyLittleThingGoblin(MetaGoblin):

    '''
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'prettylittlething goblin'

    def run(self):
        html = self.get_html(self.args['url'])
        for parsed in {p.group() for p in re.finditer(r'https://cdn\-img\.prettylittlething\.com[^" \n]+', html)}:
            self.loot(parsed, clean=True)
            sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
