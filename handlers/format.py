import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class FormatGoblin(MetaGoblin):

    '''
    mode options:
        - scan : scan for higher resolutions
    format option:
        - w (width)
        - h (height)
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'format goblin'

    def run(self, url, n=1500, inc=10):
        url = re.split(r'h_\d+,w_\d+', self.url)
        if self.args['mode'] == 'scan':
            while True:
                if n % 250 == 0:
                    print(n)
                if self.args['format'] == 'w':
                    url = f'{url[0]}h_65535,w_{n}{url[1]}'
                else:
                    url = f'{url[0]}h_{n},w_65535{url[1]}'
                self.loot(url, self.path_main, filename=f'{extract_filename(url[1])}_{self.mode}{n}')
                n += inc
                sleep(self.args['tickrate'])
        else:
            if self.args['format'] == 'w':
                self.loot(f'{url[0]}h_65535,w_{n}{url[1]}', self.path_main)
            else:
                self.loot(f'{url[0]}h_{n},w_65535{url[1]}', self.path_main)
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
