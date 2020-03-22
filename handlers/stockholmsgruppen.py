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
        if 'amazonaws' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(r'<img data-url-h\d+="//stockholmsgruppen.s3.amazonaws.com/images/[\w-]+"', self.args['url'])
        for link in links:
            self.loot(re.sub(r'<img data-url-h\d+="//', '', link.group()[:-1]))
            sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
