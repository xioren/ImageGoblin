import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class StockholmsgruppenGoblin(MetaGoblin):

    '''
    url types:
        - webpage
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, tickrate, verbose, nodl)
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'stockholmsgruppen goblin'

    def run(self):
        # NOTE: the h#### varies from profile to profile
        matches = re.finditer(r'<img data-url-h\d+="//stockholmsgruppen.s3.amazonaws.com/images/[\w-]+"',
                              self.get_html(self.url))
        for match in matches:
            link = re.sub(r'<img data-url-h\d+="//', '', match.group()[:-1])
            self.loot(link)
            sleep(self.tickrate)
