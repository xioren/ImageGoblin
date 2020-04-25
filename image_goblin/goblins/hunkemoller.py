import re

from goblins.meta import MetaGoblin


# NOTE: uses different urls structure depending on region
# alternate: https://www.hunkemoller.co.uk/on/demandware.static/-/Sites-hkm-master/default/images/large/
# alternate: https://hunkemoller.by/media/img/hkm/


class HunkemollerGoblin(MetaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.modifiers = ('_1', '_2', '_3', '_4', '_5')
        self.urls_types = re.compile('(?:akamaized|img/hkm|demandware)')
        self.iter_pat = re.compile(r'_\d(?=\.jpg)')
        self.img_pat = re.compile(r'(?:\d+_\d(_normal)?\.jpg)')
        self.url_pat = re.compile(r'(?:https?://images-hunkemoller\.akamaized.net/[^"\s]+' \
                                  r'|https?://hunkemoller\.[a-z]/media/img/hkm/[^"\s]+' \
                                  r'|https://www\.hunkemoller\.[^"\s]+demandware[^"\s]+)')
        self.url_base = 'https://images-hunkemoller.akamaized.net/original/'

    def __str__(self):
        return 'hunkemoller goblin'

    def __repr__(self):
        return 'hunkemoller'

    def extract_parts(self, url):
        '''split the url into id, end'''
        return re.split(self.iter_pat, url.replace('_normal', ''))

    def isolate(self, url):
        '''isolate the end of the url'''
        return re.search(r'(?<=/)[^/]+\.jpe?g', url).group()

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if re.search(self.urls_types, target):
                urls = [target]
            else:
                urls = self.extract_by_regex(self.url_pat, target)
            for url in urls:
                if not re.search(self.img_pat, url):
                    continue
                id, url_end = self.extract_parts(self.isolate(url))
                for mod in self.modifiers:
                    self.collect(f'{self.url_base}{id}{mod}{self.parser.dequery(url_end)}')
        self.loot()
