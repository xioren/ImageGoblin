import re

from goblins.meta import MetaGoblin


# NOTE: uses different urls structure depending on region
# alternate: https://www.hunkemoller.co.uk/on/demandware.static/-/Sites-hkm-master/default/images/large/
# alternate: https://hunkemoller.by/media/img/hkm/


class HunkemollerGoblin(MetaGoblin):

    NAME = 'hunkemoller goblin'
    ID = 'hunkemoller'
    MODIFIERS = ('_1', '_2', '_3', '_4', '_5')
    URL_BASE = 'https://images-hunkemoller.akamaized.net/original/'

    URL_TYPES = re.compile('(?:akamaized|img/hkm|demandware)')
    ITER_PAT= re.compile(r'_\d(?=\.jpg)')
    IMG_PAT = re.compile(r'(?:\d+_\d(_normal)?\.jpg)')
    URL_PAT = re.compile(r'(?:https?://images-hunkemoller\.akamaized.net/[^"\s]+' \
                         r'|https?://hunkemoller\.[a-z]/media/img/hkm/[^"\s]+' \
                         r'|https://www\.hunkemoller\.[^"\s]+demandware[^"\s]+)')

    def __init__(self, args):
        super().__init__(args)

    def extract_parts(self, url):
        '''split the url into id, end'''
        return re.split(self.ITER_PAT, url.replace('_normal', ''))

    def isolate(self, url):
        '''isolate the end of the url'''
        return re.search(r'(?<=/)[^/]+\.jpe?g', url).group()

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')

        for target in self.args['targets'][self.ID]:
            if re.search(self.URL_TYPES, target):
                urls = [target]
            else:
                urls = self.parser.extract_by_regex(self.get(target).content, self.URL_PAT)

            for url in urls:
                if not re.search(self.IMG_PAT, url):
                    continue

                id, url_end = self.extract_parts(self.isolate(url))

                for mod in self.MODIFIERS:
                    self.collect(f'{self.URL_BASE}{id}{mod}{self.parser.dequery(url_end)}')

        self.loot()
