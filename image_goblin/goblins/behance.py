import re

from goblins.meta import MetaGoblin


class BehanceGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'behance goblin'
    ID = 'behance'
    URL_PAT = r'https?://mir-s3-cdn-cf\.behance\.net/project_modules/[\w/\.]+\.[A-Za-z]+'
    SIZE_PAT = r'fs|1400(_opt_1)*|max_1200|disp'
    SIZES = ('max_3840', 'fs', '1400', 'max_1200', 'disp')

    def __init__(self, args):
        super().__init__(args)

    def fit(self, url, size):
        '''sub size into url'''
        return re.sub(self.SIZE_PAT, size, url)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        self.toggle_collecton_type()
        no_duplicates = []

        for target in self.args['targets'][self.ID]:
            if 'mir-s3-cdn' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls = [target]
            else:
                self.headers.update({'Cookie': 'ilo0=true'})
                urls = self.parser.extract_by_regex(self.get(target).content, self.URL_PAT)

            for url in urls:
                filename = self.parser.extract_filename(url)
                if filename in no_duplicates:
                    continue
                no_duplicates.append(filename)

                for size in self.SIZES:
                    new_url = self.fit(url, size)
                    if self.get(new_url).code:
                        self.collect(new_url)
                        break

        self.loot()
