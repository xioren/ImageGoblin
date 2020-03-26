import re
from handlers.meta_goblin import MetaGoblin


class TallyWeijlGoblin(MetaGoblin):

    '''
    accepts:
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'tally weijl goblin'

    def run(self):
        if '/img/' in self.args['url']:
            links = []
            if not self.args['silent']:
                print(f'[{self.__str__()}] <WARNING> url type not supported')
        else:
            links = self.extract_links(r'https*://www\.tally\-weijl\.com/img/[^" ]+\.jpg', self.args['url'])
        for link in links:
            self.collect(re.sub(r'img/\d+/\d+', 'img/1800/1800', link))
        self.loot()
