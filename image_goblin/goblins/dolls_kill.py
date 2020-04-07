import re

from goblins.meta import MetaGoblin


class DollsKillGoblin(MetaGoblin):
    '''accepts:
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'img src="https?://media\.dollskill\.com[^"]+\-\d+.jpg'

    def __str__(self):
        return 'dolls kill goblin'

    def __repr__(self):
        return 'dollskill'

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'media.dollskill' in target:
                url = []
                if not self.args['silent']:
                    print(f'[{self.__str__()}] <WARNING> image urls not supported')
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                self.collect(re.sub(r'\d+\.jpg', '1.jpeg', url).lstrip('img src="'))
        self.loot()
