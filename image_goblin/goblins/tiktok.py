import json

from os.path import join

from goblins.meta import MetaGoblin


# QUESTION: what is secUid for?
# TODO: handle single posts?
# NOTE: remove watermark with "https://api2.musical.ly/aweme/v1/playwm/?video_id=" (untested)
# NOTE: type=1 recent posts?


class TikTokGoblin(MetaGoblin):
    '''accepts:
        - video*
        - webpage
    '''

    NAME = 'tiktok goblin'
    ID = 'tiktok'
    API_URL = 'https://www.tiktok.com/api'
    API_USER_URL = API_URL + '/user/detail/?uniqueId={}&language=en'
    API_ITEM_URL = API_URL + '/item_list/?count={}&id={}&maxCursor={}&minCursor=0&sourceType=8&language=en'

    def __init__(self, args):
        super().__init__(args)
        self.MIN_SIZE = 0
        self.count = self.args['posts'] if self.args['posts'] < 99 else 99

    def run(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            username = self.parser.safe_search(r'(?<=@)[^/]+', url)
            user_dir = join(self.path_main, username)
            self.make_dirs(user_dir)

            if 'ibyteimg' in target or 'tiktokcdn' in target:
                urls.append(target)
                self.logger.log(2, self.NAME, 'WARNING', 'video urls not fully supported', once=True)
            else:
                # get user id using username
                response = json.loads(self.get(self.API_USER_URL.format(username)).content)

                if 'userInfo' in response:
                    user_id = response['userInfo']['user']['id']
                    urls.append(response['userInfo']['user']['avatarLarger'])

                    max_cursor = 0

                    while True:
                        # retrieve posts
                        response = json.loads(self.get(self.API_ITEM_URL.format(self.count, user_id, max_cursor)).content)

                        for item in response.get('items', ''):
                            urls.append(item['video']['cover'])
                            urls.append(item['video']['downloadAddr'])

                        if not response.get('hasMore') or self.count < 99:
                            break

                        max_cursor = response['maxCursor']
                        # NOTE: fetching more only works when keeping min_cursor at 0
                        # min_cursor = response['minCursor']

                        self.delay()

        for url in urls:
            self.collect(url)

        self.loot(save_loc=user_dir)
        if not self.args['nodl']:
            self.move_vid(user_dir)
