import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class StockholmsgruppenGoblin(MetaGoblin):

    '''
    accepts:
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'stockholmsgruppen goblin'

    def run(self):
        # NOTE: the h#### varies from profile to profile
        matches = re.finditer(r'<img data-url-h\d+="//stockholmsgruppen.s3.amazonaws.com/images/[\w-]+"',
                              self.get_html(self.args['url']))
        for match in matches:
            link = re.sub(r'<img data-url-h\d+="//', '', match.group()[:-1])
            self.loot(link)
            sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
