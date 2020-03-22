import re
from time import sleep
from handlers.meta_goblin import MetaGoblin

# removing /dw/image/v2/AAYL_PRD give original image, while leaving it in allow resizing
# TODO: handle both image and webpage urls

class GammaGoblin(MetaGoblin):

    '''
    for on.demandware variants
    accepts:
        - image
        - webpage
    generic backend for:
        - boux avenue
        - etam
        - hunkemoller
        - sandro
        - springfield
        - womens secret
    '''

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        return re.search(self.pattern, url).group()

    def prep(self, url):
        # NOTE: unused
        if 'images' in url:
            return re.sub(r'dw/image/v\d/[A-Z]+_[A-Z]+/', '', re.sub(r'default/\w+/', 'default/images/', url))
        else:
            return re.sub(r'dw/image/v\d/[A-Z]+_[A-Z]+/', '', re.sub(r'default/\w+/', 'default/', url))

    def run(self):
        if '.jpg' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(fr'{self.pattern}\w+\.jpe*g', self.args['url'])
        for link in links:
            id = self.extract_id(link)
            # link = dequery(re.sub(fr'{id}(\w+)*.jpg', '', link))
            for mod in self.modifiers:
                self.loot(f'{self.base}{id}{mod}.jpg')
                sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
