import re
from handlers.meta_goblin import MetaGoblin


class DollsKillGoblin(MetaGoblin):

    '''
    accepts:
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.link_pat = r'img src="https://media.dollskill.com[^"]+\-\d+.jpg'

    def __str__(self):
        return 'dolls kill goblin'

    def run(self):
        if 'media.dollskill' in self.args['url']:
            link = []
            if not self.args['silent']:
                print(f'[{self.__str__()}] <WARNING> url type not supported')
        else:
            links = self.extract_links(self.link_pat, self.args['url'])
        for link in links:
            self.collect(re.sub(r'\d+.jpg', '1.jpeg', link).replace('img src="', ''))
        self.loot()
