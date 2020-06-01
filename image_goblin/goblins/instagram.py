import os
import re
import json

from time import sleep
from getpass import getpass
from urllib.parse import quote, urljoin
from goblins.meta import MetaGoblin


# NOTE: deprecated pagination /?__a=1


class InstagramGoblin(MetaGoblin):
    '''code inspired by:
        - https://github.com/rarcega/instagram-scraper
        - https://github.com/ytdl-org/youtube-dl
        - various stack overflow posts
    '''

    NAME = 'instagram goblin'
    ID = 'instagram'
    BASE_URL = 'https://www.instagram.com'
    LOGOUT_URL = BASE_URL + '/accounts/logout/'
    LOGIN_URL = BASE_URL + '/accounts/login/ajax/'
    SEARCH_URL = BASE_URL + '/web/search/topsearch/?query='
    POST_URL = BASE_URL + '/graphql/query/?query_hash=1451128a3ce596b72f20c738dc7f0f73&variables={}'
    MEDIA_URL = BASE_URL + '/graphql/query/?query_hash=44efc15d3c13342d02df0b5a9fa3d33f&variables={}'
    STORIES_USER_ID_URL = BASE_URL + '/graphql/query/?query_hash=c9100bf9110dd6361671f113dd02e7d6&variables={}'
    STORIES_REEL_ID_URL = BASE_URL + '/graphql/query/?query_hash=45246d3fe16ccc6577e0bd297a5db1ab&variables={}'

    def __init__(self, args):
        super().__init__(args)
        self.logged_in = False
        self.num_posts = self.args['posts'] if self.args['posts'] <= 100 else 100

    def setup(self, url):
        '''initialize user'''
        self.username = self.extract_username(url)
        self.insta_dir = os.path.join(self.path_main, self.username)
        self.vid_dir = os.path.join(self.insta_dir, 'vid')

        self.make_dirs(self.insta_dir, self.vid_dir)

    def extract_username(self, url):
        if '/p/' in url:
            shortcode = url.rstrip('/').split('/')[-1]
            variables = f'{{"shortcode":"{shortcode}","include_reel":true}}'
            response = json.loads(self.get(self.POST_URL.format(quote(variables, safe='"'))).content)
            return response['data']['shortcode_media']['owner']['reel']['owner']['username']
        else:
            return url.rstrip('/').split('/')[-1]

    def move_vid(self):
        '''move videos into seperate directory'''
        for file in os.listdir(self.insta_dir):
            if '.mp4' in file:
                os.rename(os.path.join(self.insta_dir, file), os.path.join(self.vid_dir, file))

    def authenticate(self, login):
        '''login to instagram or authenticate as guest'''
        response = self.get(self.BASE_URL, store_cookies=True)
        self.set_cookies()

        if login:
            while True:
                username = input(f'[{self.NAME}] username: ')
                password = getpass(f'[{self.NAME}] password: ')
                response = json.loads(self.post(self.LOGIN_URL, data={'username': username, 'password': password}, store_cookies=True).content)
                self.set_cookies()
                del username, password

                if 'authenticated' in response:
                    self.logged_in = True
                    self.logger.log(0, self.NAME, 'logged in')
                elif 'checkpoint_url' in response:
                    self.logger.log(0, self.NAME, 'WARNING', 'account verification required')
                    self.verify_account(response['checkpoint_url'])
                else:
                    self.logger.log(0, self.NAME, 'ERROR', 'login failed')
                    retry = input(f'[{self.NAME}] retry? (y/n): ')
                    if retry == 'y':
                        continue
                    self.logger.log(0, self.NAME, 'continuing as guest')
                break

    def logout(self):
        response = self.post(self.LOGOUT_URL, data={'csrfmiddlewaretoken': self.cookie_value("csrftoken")})

        if response.code == 200:
            self.logger.log(0, self.NAME, 'logged out')
        else:
            self.logger.log(0, self.NAME, 'ERROR', 'logout failed')

    def verify_account(self, checkpoint_url):
        '''complete security challenge to verify account'''
        # WARNING: untested
        verify_url = urljoin(self.BASE_URL, checkpoint_url)
        response = self.get(verify_url, store_cookies=True)
        self.set_cookies()

        self.headers.update(
            {
                'X-Instagram-AJAX': '1',
                'Referer': verify_url
            }
        )

        mode = input(f'[{self.NAME}] receive code via (0 - sms, 1 - email): ')
        challenge = self.post(verify_url, data= {'choice': mode}, store_cookies=True)
        self.set_cookies()

        while True:
            code = int(input(f'[{self.NAME}] enter security code: '))
            response = self.post(verify_url, data={'security_code': code}, store_cookies=True)
            self.set_cookies()
            answer = json.loads(response.content)

            if answer.get('status') == 'ok':
                self.logged_in = True
                self.logger.log(0, self.NAME, 'logged in')
            else:
                self.logger.log(0, self.NAME, 'ERROR', 'security challenge failed')
                retry = input(f'[{self.NAME}] retry? (y/n): ')
                if retry == 'y':
                    continue
                else:
                    self.logger.log(0, self.NAME, 'continuing as guest')
            break

    def get_initial_data(self):
        '''make initial request to recieve necessary variables'''
        # WARNING: deprecated
        self.extend_cookie('Cookie', 'ig_pr=1')
        response = self.get(urljoin(self.BASE_URL, self.username)).content
        if response:
            data = json.loads(re.search(r'(?<=sharedData\s=\s){.+?}(?=;)', response).group())

            if data['entry_data'].get('ProfilePage'):
                self.user_id = data['entry_data']['ProfilePage'][0]['graphql']['user']['id']
                # self.rhx_gis = response.get('rhx_gis', '3c7ca9dcefcf966d11dacf1f151335e8')
                return True
        self.logger.log(2, self.NAME, 'ERROR', 'failed to get user id')
        return False

    def get_user_id(self):
        '''make initial request to obtain user id'''
        # NOTE: temporary workaround
        response = json.loads(self.get(f'{self.SEARCH_URL}{self.username}').content)

        if response:
            self.user_id = response['users'][0]['user']['pk']
            return True

        self.logger.log(2, self.NAME, 'ERROR', 'failed to get user id')
        return False

    def parse_profile(self):
        '''collect and parse instagram posts'''
        # POST_PAT = re.compile(r'(?<="shortcode":")[^"]+')
        cursor = ''

        self.headers.update({'X-Requested-With': 'XMLHttpRequest'})

        self.logger.log(1, self.NAME, 'parsing profile', self.username)

        while True:
            variables = json.dumps(
                {
                    'id': self.user_id,
                    'first': self.num_posts,
                    'after': cursor
                }
            )

            response = json.loads(self.get(self.MEDIA_URL.format(quote(variables, safe='"'))).content)

            for edge in response['data']['user']['edge_owner_to_timeline_media']['edges']:
                self.extract_media(edge)
                if 'edge_sidecar_to_children' in edge['node']: # post has multiple images/videos
                    for inner_edge in edge['node']['edge_sidecar_to_children']['edges']:
                        self.extract_media(inner_edge)

            cursor = response['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']

            if not cursor or self.num_posts < 100:
                # end of profile or user specified finite number of posts.
                break

            sleep(self.delay)

    def extract_media(self, edge):
        '''extract media from posts'''
        image_url = edge['node']['display_url']
        video_url = edge['node'].get('video_url')
        self.collect(image_url, f'{self.username}_{self.parser.extract_filename(image_url)}')
        if video_url:
            self.collect(video_url, f'{self.username}_{self.parser.extract_filename(video_url)}')

    def get_stories(self, url):
        response = json.loads(self.get(url).content)

        for reel_media in response['data']['reels_media']:
            for item in reel_media['items']:
                url = item['display_url']
                self.collect(url, f'{self.username}_{self.parser.extract_filename(url)}')

                if 'video_resources' in item:
                    url = item['video_resources'][-1]['src']
                    self.collect(url, f'{self.username}_{self.parser.extract_filename(url)}')

    def get_main_stories(self):
        # QUESTION: POST URL??
        self.get_stories(self.POST_URL.format(quote('{{"reel_ids":["{}"],"tag_names":[],' \
        '"location_ids":[],"highlight_reel_ids":[],"precomposed_overlay":false}}'.format(self.user_id), safe='"')))

    def get_highlight_stories(self):
        response = json.loads(self.get(self.STORIES_USER_ID_URL.format(quote('{{"user_id":"{}",' \
        '"include_chaining":false,"include_reel":false,"include_suggested_users":false,' \
        '"include_logged_out_extras":false,"include_highlight_reels":true,' \
        '"include_related_profiles":false}}'.format(self.user_id), safe='"'))).content)

        higlight_stories_ids = [item['node']['id'] for item in response['data']['user']['edge_highlight_reels']['edges']]
        ids_chunks = [higlight_stories_ids[i:i + 3] for i in range(0, len(higlight_stories_ids), 3)]

        for ids_chunk in ids_chunks:
            self.get_stories(self.STORIES_REEL_ID_URL.format(quote('{{"reel_ids":[],' \
            '"tag_names":[],"location_ids":[],"highlight_reel_ids":["{}"],' \
            '"precomposed_overlay":false}}'.format('","'.join(str(x) for x in ids_chunk)), safe='"')))

    def run(self):
        # QUESTION: can authentication and user id aquisition happen with same request?
        self.authenticate(self.args['login'])

        for target in self.args['targets'][self.ID]:
            if 'cdninstagram' in target:
                self.collect(target)
                self.loot()
            else:
                self.new_collection()
                self.setup(target)
                if '/p/' in target:
                    self.logger.log(0, self.NAME, 'ERROR', 'post urls are temporarily disabled')
                else:
                    if self.args['mode'] == 'latest' or self.args['mode'] == 'recent':
                        self.num_posts = 6
                    retrieved_data = self.get_user_id()

                    if retrieved_data:
                        if self.logged_in:
                            self.logger.log(1, self.NAME, 'collecting stories')
                            self.get_main_stories()
                            if self.args['mode'] != 'latest' and self.args['mode'] != 'recent':
                                self.get_highlight_stories()

                        self.parse_profile()

                self.loot(save_loc=self.insta_dir)
                if not self.args['nodl']:
                    self.move_vid()
        if self.logged_in:
            self.logout()
